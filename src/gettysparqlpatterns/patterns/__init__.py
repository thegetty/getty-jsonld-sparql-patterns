from .archivalpatterns import patternlist as archivalpatterns
from .la_counts import patternlist as la_counts

from ..registry import SPARQLRegistry, PatternSet

archival_patterns = PatternSet(
    name="Linked.Art Archival data patterns",
    description="""A set of SPARQL patterns for getting specific bits of information from Getty-published
    archival metadata held in Linked Data.""",
)

# import the base set of archival metadata patterns
archival_patterns.import_patterns(archivalpatterns)

# to show how to add new patterns using a method, rather than importing a set
archival_patterns.add_pattern(
    name="get_images_for_a_refid",
    description="The query will find a list of VisualItem URIs for the images that fall under a specific archival component with a given refid. "
    "The expected structure is that the archival component is connected to one or more HMOs, which reference one or more images.",
    sparql_pattern="""PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?image WHERE {
  ?hmo rdfs:label ?name .
  ?hmo crm:P46i_forms_part_of/crm:P1_is_identified_by ?ident .
  ?ident crm:P190_has_symbolic_content "$refid" .
  ?ident crm:P2_has_type <https://data.getty.edu/local/thesaurus/ref-id> .
  ?hmo crm:P65_shows_visual_item ?image
} limit 1000""",
    stype="select",
)

SPARQLRegistry.register("archival", archival_patterns)


la_count_patterns = PatternSet(
    name="Counting numbers of Linked Art objects",
    description="""A set of SPARQL patterns for counting how many resources of certain types are known to the SPARQL endpoint.""",
)

# import the base set of archival metadata patterns
la_count_patterns.import_patterns(la_counts)
SPARQLRegistry.register("la_counts", la_count_patterns)
