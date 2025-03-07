from .registry import SPARQLRegistry, PatternSet
from .patterns import archival_patterns

# VERSION number
import importlib.metadata

__version__ = importlib.metadata.version("gettysparqlpatterns")

# * imports with a minimal list:
__all__ = [
    "SPARQLRegistry",
    "PatternSet",
    "archival_patterns",
    "__version__",
]
