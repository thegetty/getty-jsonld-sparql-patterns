from .utilities import (
    SPARQLPatternsError,
    NoSuchPatternError,
    RequiredParametersMissingError,
    NoSPARQLEndpointSetError,
    SPARQLResponseObj,
    SPARQLURI,
    SPARQLLiteral,
)
from .registry import (
    SPARQLRegistry,
    PatternSet,
)

from .patterns import archival_patterns

# VERSION number
import importlib.metadata

__version__ = importlib.metadata.version("gettysparqlpatterns")

# * imports with a controlled list:
__all__ = [
    "SPARQLRegistry",
    "PatternSet",
    "archival_patterns",
    "SPARQLPatternsError",
    "NoSuchPatternError",
    "RequiredParametersMissingError",
    "NoSPARQLEndpointSetError",
    "SPARQLResponseObj",
    "SPARQLURI",
    "SPARQLLiteral",
    "__version__",
]
