# from .archivalpatterns import patternlist as archivalpatterns
import json
from importlib.resources import files, as_file
import gettysparqlpatterns.data

from .la_counts import patternlist as la_counts
from ..registry import SPARQLRegistry, PatternSet


def _load_from_package(patternset, datafilename):
    source = files(gettysparqlpatterns.data).joinpath(datafilename)
    with as_file(source) as jdoc:
        pl = json.loads(jdoc.read_text())
        patternset.import_patterns(pl)


def pattern_load():
    # Load data from a patternset exported as JSON
    archival_patterns = PatternSet(
        name="Linked.Art Archival data patterns",
        description="""A set of SPARQL patterns for getting specific bits of information from Getty-published
        archival metadata held in Linked Data.""",
    )

    # import the base set of archival metadata patterns
    _load_from_package(archival_patterns, "archival_patterns.json")
    SPARQLRegistry.register("archival", archival_patterns)

    # Load the Linked Art count sparql patterns from an object:
    la_count_patterns = PatternSet(
        name="Counting numbers of Linked Art objects",
        description="""A set of SPARQL patterns for counting how many resources of certain types are known to the SPARQL endpoint.""",
    )

    # import the base set of archival metadata patterns
    la_count_patterns.import_patterns(la_counts)
    SPARQLRegistry.register("la_counts", la_count_patterns)
