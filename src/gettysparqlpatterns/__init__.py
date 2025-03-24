from .utilities import (
    SPARQLResponseObj,
    SPARQLURI,
    SPARQLLiteral,
)
from .exceptions import (
    SPARQLPatternsError,
    NoSuchPatternError,
    RequiredParametersMissingError,
    NoSPARQLEndpointSetError,
    NoPatternsFoundError,
    PatternNotSetError,
)
import gettysparqlpatterns.data
from .registry import SPARQLRegistry, PatternSet

# Register built in patterns
from .patterns import pattern_load

# VERSION number
import importlib.metadata

__version__ = importlib.metadata.version("gettysparqlpatterns")

# * imports with a controlled list:
__all__ = [
    "SPARQLRegistry",
    "PatternSet",
    "SPARQLPatternsError",
    "NoSuchPatternError",
    "NoPatternsFoundError",
    "RequiredParametersMissingError",
    "NoSPARQLEndpointSetError",
    "PatternNotSetError",
    "SPARQLResponseObj",
    "SPARQLURI",
    "SPARQLLiteral",
    "__version__",
]

pattern_load()
