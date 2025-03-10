import logging

from string import Template
from typing import Literal, Callable

# Workaround for the Template.get_identifiers only in py3.11+
import re

from .utilities import (
    NoSuchPatternError,
    RequiredParametersMissingError,
    NoSPARQLEndpointSetError,
    SPARQLResponseObj,
    SPARQLURI,
    SPARQLLiteral,
)


logger = logging.getLogger(__name__)


class SPARQLRegistry:
    _registry = {}
    _descriptions = {}

    @classmethod
    def register(cls, name, patternset):
        cls._registry[name] = patternset

    @classmethod
    def get_patternsets(cls, name=None):
        if not name:
            return cls._registry
        else:
            return cls._registry.get(name)

    @classmethod
    def list_pattern_names(cls):
        return sorted(list(cls._registry.keys()))

    @classmethod
    def browse_patternsets(cls):
        return [(x, y, y.description) for x, y in cls._registry.items()]


class BasePattern:
    def __init__(
        self,
        name: str,
        sparql_pattern: str,
        stype: Literal["ask", "select", "construct", "count"],
        description: str | None = None,
        **kwargs,
    ):
        self.name = name
        self.description = (
            description  # A description about the purpose and use of this pattern.
        )
        self.sparql_pattern = ""
        self.stype = stype
        self.keyword_parameters = []
        self._set_pattern(
            sparql_pattern
        )  # Find out what parameters are in the sparql query, if any

    def _set_pattern(self, sparql_pattern):
        try:
            self.sparql_pattern = Template(sparql_pattern)
            # py3.11+
            #  self.keyword_parameters = self.sparql_pattern.get_identifiers()
            self.keyword_parameters = list(
                set(
                    re.findall(
                        r"\$([a-z_0-9]+)\s*",
                        self.sparql_pattern.template,
                        re.IGNORECASE | re.MULTILINE,
                    )
                )
            )
        except ValueError as e:
            logger.error(f"An error occurred attempting to set the sparql template {e}")
            raise e

    def get_query(self, **kwargs):
        if self.sparql_pattern:
            return self.sparql_pattern.substitute(kwargs)


class PatternSet:
    def __init__(
        self,
        name: str,
        description: str | None = None,
        sparql_client_method: Callable[[str], dict | str] = None,
    ):
        self.name = name
        self.description = description or "No description given."
        self.sparql_client_method = sparql_client_method
        self._patterns = {}

    def set_sparql_client_method(self, sparql_client_method):
        self.sparql_client_method = sparql_client_method

    def add_pattern(
        self,
        name: str,
        sparql_pattern: str,
        stype: Literal["ask", "select", "construct", "count"],
        description: str | None = None,
    ):
        self._patterns[name] = BasePattern(
            name=name,
            description=description or "No description given",
            sparql_pattern=sparql_pattern,
            stype=stype,
        )

    def browse_patterns(self, by_type=None):
        if not by_type:
            return [
                (name, pattern.description, pattern, pattern.keyword_parameters)
                for name, pattern in self._patterns.items()
            ]
        else:
            return [
                (name, pattern.description, pattern, pattern.keyword_parameters)
                for name, pattern in self._patterns.items()
                if pattern.stype == by_type
            ]

    def list_patterns(self, by_type=None):
        if not by_type:
            return [name for name, pattern in self._patterns.items()]
        else:
            return [
                name
                for name, pattern in self._patterns.items()
                if pattern.stype == by_type
            ]

    def get_pattern(self, name):
        return self._patterns.get(name)

    def export_patterns(self):
        return [
            {
                "name": name,
                "description": pattern.description,
                "sparql_pattern": pattern.sparql_pattern.template,
                "stype": pattern.stype,
                "keyword_parameters": pattern.keyword_parameters,
            }
            for name, pattern in self._patterns.items()
        ]

    def import_patterns(self, patterns: list, clear_before_import: bool = True):
        if _loaded := {p["name"]: BasePattern(**p) for p in patterns if p}:
            if clear_before_import:
                self._patterns = _loaded
            else:
                self._patterns.update(_loaded)

    def format_pattern(self, name, **kwargs):
        if pattern := self._patterns.get(name):
            if not all([x in kwargs for x in pattern.keyword_parameters]):
                raise RequiredParametersMissingError(
                    f"Query requires the following parameters: {pattern.keyword_parameters}"
                )
            return pattern.get_query(**kwargs)
        else:
            raise NoSuchPatternError(f"'{name} not found'")

    def run_pattern(
        self, name: str, sparql_client_method: Callable[[str], dict] = None, **kwargs
    ):
        if not sparql_client_method:
            sparql_client_method = self.sparql_client_method

        if sparql_client_method is None:
            raise NoSPARQLEndpointSetError()

        query = self.format_pattern(name, **kwargs)
        resp = sparql_client_method(query)
        match resp:
            case {"head": {}, "boolean": resp}:
                return resp
            case {"head": {"vars": [*_]}, "results": {"bindings": [*results]}}:
                # assume that any results returned is a truthy response
                if self._patterns.get(name).stype == "count":
                    match results:
                        case [
                            {
                                "count": {
                                    "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                                    "type": "literal",
                                    "value": count,
                                }
                            }
                        ]:
                            return int(count)

                # Process the response as a standard SELECT response
                parsed_results = []
                for resultrow in results:
                    row = {}
                    for k, v in resultrow.items():
                        match v:
                            case {
                                "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                                "type": "literal",
                                "value": value,
                            }:
                                row[k] = int(value)
                            case {"type": "uri", "value": value}:
                                row[k] = SPARQLURI(value)
                            case {"type": "literal", "value": value, **other}:
                                datatype = other.get("datatype")
                                row[k] = SPARQLLiteral(value, datatype)
                            case {"type": othertype, "value": value, **other}:
                                datatype = other.get("datatype")
                                row[k] = SPARQLResponseObj(
                                    value, othertype, datatype=datatype
                                )
                    parsed_results.append(row)
                return parsed_results
            case other:
                return other
