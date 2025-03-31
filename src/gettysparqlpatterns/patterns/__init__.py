# from .archivalpatterns import patternlist as archivalpatterns
from ..utilities import load_from_package

from ..registry import SPARQLRegistry, PatternSet


def pattern_load():
    # Load data from a patternset exported as JSON
    archival_patterns = PatternSet(from_builtin="archival_patterns.json")
    SPARQLRegistry.register("archival", archival_patterns)
