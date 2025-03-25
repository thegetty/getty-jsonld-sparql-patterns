import logging
import requests

from string import Template
from typing import Literal, Callable

# Workaround for the Template.get_identifiers only in py3.11+
import re

from .utilities import (
    parsed_sparql_response,
)
from .exceptions import (
    NoSuchPatternError,
    RequiredParametersMissingError,
    NoSPARQLEndpointSetError,
    NoPatternsFoundError,
    PatternNotSetError,
)


logger = logging.getLogger(__name__)


def _match(obj, by_type, by_applies_to):
    if not by_type and not by_applies_to:
        return True
    elif by_type is not None:
        if by_applies_to not in [None, []]:
            if by_type == obj.stype and by_applies_to in obj.applies_to:
                return True
        elif by_type == obj.stype:
            return True
    elif by_applies_to not in [None, []] and by_applies_to in obj.applies_to:
        return True
    return False


class SPARQLRegistry:
    _registry = {}

    @classmethod
    def register(cls, name, patternset):
        cls._registry[name] = patternset

    @classmethod
    def get_patternsets(cls):
        return cls._registry

    @classmethod
    def get_patternset(cls, name):
        p = cls._registry.get(name)
        if p is not None:
            return p
        else:
            raise NoSuchPatternError(f"{name} is not a known patternset.")

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
        default_values: dict | None = None,
        applies_to: list | None = None,
        sparql_client_method: Callable[[str], dict | str] = None,
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

        # Allow for default values to be set (useful for LIMIT or SERVICE URIs)
        self.default_values = {}
        if isinstance(default_values, dict):
            self.default_values = default_values

        self.applies_to = []
        if applies_to:
            match applies_to:
                case [*_]:
                    self.applies_to = applies_to
                case _:
                    self.applies_to = [applies_to]

        self.sparql_client_method = sparql_client_method

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
        # Set with defaults, and then update with the passed parameters
        q_kwargs = self.default_values.copy()
        q_kwargs.update(kwargs)

        if not all([x in q_kwargs for x in self.keyword_parameters]):
            raise RequiredParametersMissingError(
                f"Query requires the following parameters: {self.keyword_parameters}"
            )

        if self.sparql_pattern:
            logger.debug(
                f"Templating '{self.name}' sparql pattern with parameters {q_kwargs}"
            )
            return self.sparql_pattern.substitute(q_kwargs)
        else:
            raise PatternNotSetError("The sparql_pattern is not set and cannot be run.")

    def run(self, sparql_client_method: Callable[[str], dict] = None, **kwargs):
        if not sparql_client_method:
            sparql_client_method = self.sparql_client_method

        if sparql_client_method is None:
            raise NoSPARQLEndpointSetError()

        query = self.get_query(**kwargs)
        return parsed_sparql_response(sparql_client_method(query), self.stype)


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
        self._update_patterns_w_sparql_method()

    def use_lodgateway_for_queries(self, lodgateway):
        if lodgateway.capabilities.get("JSON-LD") is True:
            self.sparql_client_method = lodgateway.sparql
            self._update_patterns_w_sparql_method()
        else:
            raise Exception(
                f"LOD Gateway {lodgateway.object_base} does not report having JSON-LD functionality, so may not have SPARQL"
            )

    def _update_patterns_w_sparql_method(self):
        if self.sparql_client_method:
            for k, v in self._patterns.items():
                v.sparql_client_method = self.sparql_client_method

    def add_pattern(
        self,
        name: str,
        sparql_pattern: str,
        stype: Literal["ask", "select", "construct", "count"],
        description: str | None = None,
        default_values: dict | None = None,
        applies_to: list | None = None,
    ):
        self._patterns[name] = BasePattern(
            name=name,
            description=description or "No description given",
            sparql_pattern=sparql_pattern,
            stype=stype,
            sparql_client_method=self.sparql_client_method,
            default_values=default_values,
        )

    def browse_patterns(self, by_type=None, by_applies_to=None):
        return [
            (name, pattern.description, pattern, pattern.keyword_parameters)
            for name, pattern in self._patterns.items()
            if _match(pattern, by_type, by_applies_to)
        ]

    def list_patterns(self, by_type=None, by_applies_to=None):
        return [
            name
            for name, pattern in self._patterns.items()
            if _match(pattern, by_type, by_applies_to)
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
                "default_values": pattern.default_values,
                "applies_to": pattern.applies_to,
            }
            for name, pattern in self._patterns.items()
        ]

    def import_patterns(self, patterns: list, add_to_existing: bool = False):
        if not patterns:
            raise NoPatternsFoundError("Cannot import patterns from an empty object")
        try:
            if _loaded := {p["name"]: BasePattern(**p) for p in patterns if p}:
                if add_to_existing:
                    self._patterns.update(_loaded)
                else:
                    self._patterns = _loaded

                self._update_patterns_w_sparql_method()
        except (ValueError, TypeError):
            raise NoPatternsFoundError(
                "Could not interpret the data provided as a list of patterns to import."
            )

    def import_patterns_from_url(self, url: str, add_to_existing: bool = False):
        try:
            patterns = requests.get(url).json()
            if isinstance(patterns, list):
                self.import_patterns(patterns, add_to_existing)
            else:
                raise NoPatternsFoundError(
                    f"Could not find a suitable patternset JSON at {url}"
                )

        except requests.exceptions.JSONDecodeError:
            raise NoSuchPatternError("There are no patterns at that URL")

    def format_pattern(self, name, **kwargs):
        if pattern := self._patterns.get(name):
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
        return parsed_sparql_response(
            sparql_client_method(query), self._patterns.get(name).stype
        )

    # Ducktype a list
    def __iter__(self):
        return iter(self._patterns.values())

    def __len__(self):
        return len(self._patterns)

    def __getitem__(self, index):
        return list(self._patterns.values())[index]
