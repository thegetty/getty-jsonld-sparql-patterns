import logging
import requests

from string import Template
from typing import Literal, Callable

# Workaround for the Template.get_identifiers only in py3.11+
import re

from .utilities import parsed_sparql_response, load_from_package, list_available

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
    def register(cls, name: str, patternset):
        cls._registry[name] = patternset

    @classmethod
    def get_patternsets(cls):
        return cls._registry

    @classmethod
    def get_patternset(cls, name: str | None = None, url: str | None = None):
        p = cls._registry.get(name)
        if p is not None:
            return p
        elif url is not None:
            for k, v in cls._registry.items():
                if v.url == url:
                    return v
        else:
            raise NoSuchPatternError(f"{name} is not a known patternset.")

    @classmethod
    def list_pattern_names(cls):
        return sorted(list(cls._registry.keys()))

    @classmethod
    def browse_patternsets(cls):
        return [(x, y, y.description) for x, y in cls._registry.items()]

    @classmethod
    def load_from_preset(cls, name: str, pkg_name: str):
        patternset = PatternSet(name=name)
        load_from_package(patternset, pkg_name)
        cls.register(name, patternset)
        return patternset

    @classmethod
    def remove_patternset(cls, name: str):
        del cls._registry[name]

    @classmethod
    def list_available_patternset_presets(cls):
        return list_available()


class BasePattern:
    def __init__(
        self,
        name: str,
        sparql_pattern: str,
        stype: Literal["ask", "select", "construct", "count"],
        description: str | None = None,
        default_values: dict | None = None,
        applies_to: list | None = None,
        ask_filter: (
            bool | None
        ) = None,  # if used as a filter, which bool is the default 'allowed' value
        sparql_client_method: Callable[[str], dict | str] = None,
        framing: dict | None = None,
        profile_uri: str | None = None,
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

        # optional, only used by ask filter
        self.ask_filter = ask_filter
        if self.stype == "ask" and self.ask_filter is None:
            logger.warning(
                "The pattern is an 'ask' type, but no allowed filter was added. Defaulting to 'True' as allowed."
            )
            self.ask_filter = True

        self.sparql_client_method = sparql_client_method

        self.framing = framing
        self.profile_uri = profile_uri

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

    def filter(self, sparql_client_method: Callable[[str], dict] = None, **kwargs):
        if self.stype != "ask":
            raise NotImplementedError(
                "The 'filter' method can only be run with 'ask' type queries"
            )
        if not sparql_client_method:
            sparql_client_method = self.sparql_client_method

        if sparql_client_method is None:
            raise NoSPARQLEndpointSetError()

        query = self.get_query(**kwargs)
        return self.ask_filter == parsed_sparql_response(
            sparql_client_method(query), self.stype
        )


class PatternSet:
    def __init__(
        self,
        name: str = "",
        description: str | None = None,
        from_json: dict | None = None,
        from_url: str | None = None,
        from_builtin: str | None = None,
        sparql_client_method: Callable[[str], dict | str] = None,
    ):
        self.name = ""
        self.description = ""
        self._patterns = {}
        self.url = from_url
        self.sparql_client_method = sparql_client_method

        if from_url is None and from_builtin is None and from_json is None:
            self.name = name
            self.description = description or "No description given."
        elif from_url:
            self.import_patterns_from_url(from_url, add_to_existing=False)
        elif from_json:
            self.import_patterns(from_json, add_to_existing=False)
        else:
            load_from_package(self, from_builtin)

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
        ask_filter: bool | None = None,
        framing: dict | None = None,
        profile_uri: str | None = None,
    ):
        self._patterns[name] = BasePattern(
            name=name,
            description=description or "No description given",
            sparql_pattern=sparql_pattern,
            stype=stype,
            sparql_client_method=self.sparql_client_method,
            default_values=default_values,
            ask_filter=ask_filter,
            framing=framing,
            profile_uri=profile_uri,
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
        return {
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "patterns": [
                {
                    "name": name,
                    "description": pattern.description,
                    "sparql_pattern": pattern.sparql_pattern.template,
                    "stype": pattern.stype,
                    "keyword_parameters": pattern.keyword_parameters,
                    "default_values": pattern.default_values,
                    "applies_to": pattern.applies_to,
                    "ask_filter": pattern.ask_filter,
                    "framing": pattern.framing,
                    "profile_uri": pattern.profile_uri,
                }
                for name, pattern in self._patterns.items()
            ],
        }

    def _load_patterns(self, patterns, add_to_existing):
        if _loaded := {p["name"]: BasePattern(**p) for p in patterns if p}:
            if add_to_existing:
                self._patterns.update(_loaded)
            else:
                self._patterns = _loaded

            self._update_patterns_w_sparql_method()

    def import_patterns(self, patterns_data: list, add_to_existing: bool = False):
        if not patterns_data or (
            not isinstance(patterns_data, list) and "patterns" not in patterns_data
        ):
            raise NoPatternsFoundError("Cannot import patterns from an empty object")
        try:
            match patterns_data:
                case {"name": name, "description": description, "patterns": patterns}:
                    if add_to_existing is False:
                        # overwrite data
                        self.name = name
                        self.description = description
                        if "url" in patterns_data:
                            self.url = patterns_data["url"]
                        self._load_patterns(patterns, add_to_existing)
                case [*_]:
                    self._load_patterns(patterns_data, add_to_existing)
                case _:
                    raise ValueError("Data not acceptable")
        except (ValueError, TypeError):
            raise NoPatternsFoundError(
                "Could not interpret the data provided as a list of patterns to import."
            )

    def import_patterns_from_url(self, url: str, add_to_existing: bool = False):
        try:
            patterns_data = requests.get(url).json()

            match patterns_data:
                case {"name": name, "description": description, "patterns": patterns}:
                    if add_to_existing is False:
                        # overwrite data
                        self.name = name
                        self.description = description
                        self.url = url
                        self._load_patterns(patterns, add_to_existing)
                case [*_]:
                    self.url = url
                    self._load_patterns(patterns_data, add_to_existing)
                case _:
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
