# Getty SPARQL Patterns
A python library of SPARQL queries for use with the published data structures and ontologies in use at the Getty and held in public SPARQLable endpoints.

## Example Usage:

The key class is the `SPARQLRegistry`:

```
Python 3.10.5 (v3.10.5:f377153967, Jun  6 2022, 12:36:10) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from gettysparqlpatterns import SPARQLRegistry
```

This class can be used directly, and contains references to all the pattern sets within this module. The methods `browse_patternsets` and `list_patternsets` can be used to see the top-level groupings and what sort of SPARQL patterns they hold:

```
>>> SPARQLRegistry.browse_patternsets()
[('archival', <gettysparqlpatterns.registry.PatternSet object at 0x109456020>, 'A set of SPARQL patterns for getting specific bits of information from Getty-published\n    archival metadata held in Linked Data.'), ('la_counts', <gettysparqlpatterns.registry.PatternSet object at 0x10975bdc0>, 'A set of SPARQL patterns for counting how many resources of certain types are known to the SPARQL endpoint.')]
>>> SPARQLRegistry.list_pattern_names()
['archival', 'la_counts']
```

Each top-level pattern set holds one or more patterns, and these can be listed or browsed as before using the following methods:

```
>>> archival = SPARQLRegistry.get_patternsets("archival")
>>> archival.list_patterns()
['inf_hmo_not_ready', 'inf_not_ready', 'hmo_not_ready', 'hmo_has_component', 'hmo_list_components', 'list_collections', 'get_images_for_a_refid']


>>> archival.browse_patterns()
[('inf_hmo_not_ready', 'Given a Linked Art HumanMadeObject or a InformationObject URI, run an ASK query to see if it is for preview only and not intended for production.', <gettysparqlpatterns.registry.BasePattern object at 0x109759240>, ['URI']), ('inf_not_ready', 'Given a Linked Art InformationObject URI run an ASK query to see if it is for preview only and not intended for production.', <gettysparqlpatterns.registry.BasePattern object at 0x109758520>, ['URI']), ('hmo_not_ready', 'Given a Linked Art HumanMadeObject URI run an ASK query to see if it is for preview only and not intended for production.', <gettysparqlpatterns.registry.BasePattern object at 0x10975bd00>, ['URI']), ('hmo_has_component', '', <gettysparqlpatterns.registry.BasePattern object at 0x10975bb80>, ['URI']), ('hmo_list_components', '', <gettysparqlpatterns.registry.BasePattern object at 0x10975bc40>, ['URI']), ('list_collections', 'List all the published collections (top-level records)', <gettysparqlpatterns.registry.BasePattern object at 0x1097595d0>, []), ('get_images_for_a_refid', 'The query will find a list of VisualItem URIs for the images that fall under a specific archival component with a given refid. The expected structure is that the archival component is connected to one or more HMOs, which reference one or more images.', <gettysparqlpatterns.registry.BasePattern object at 0x1096c8940>, ['refid'])]

# The patterns can be listed which conform to a certain response type ('ask', 'select', 'construct', or 'count')
>>> archival.browse_patterns("ask")
[('inf_hmo_not_ready', 'Given a Linked Art HumanMadeObject or a InformationObject URI, run an ASK query to see if it is for preview only and not intended for production.', <gettysparqlpatterns.registry.BasePattern object at 0x109759240>, ['URI']), ('inf_not_ready', 'Given a Linked Art InformationObject URI run an ASK query to see if it is for preview only and not intended for production.', <gettysparqlpatterns.registry.BasePattern object at 0x109758520>, ['URI']), ('hmo_not_ready', 'Given a Linked Art HumanMadeObject URI run an ASK query to see if it is for preview only and not intended for production.', <gettysparqlpatterns.registry.BasePattern object at 0x10975bd00>, ['URI']), ('hmo_has_component', '', <gettysparqlpatterns.registry.BasePattern object at 0x10975bb80>, ['URI'])]


>>> archival.list_patterns("select")
['hmo_list_components', 'list_collections', 'get_images_for_a_refid']
```

To run these queries, the pattern set can return a formatted SPARQL query for a given pattern and parameters if required:

```
>>> print(archival.format_pattern("get_images_for_a_refid", refid="3bff80eb8006ef6630a072ae102fe727"))
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?image WHERE {
  ?hmo rdfs:label ?name .
  ?hmo crm:P46i_forms_part_of/crm:P1_is_identified_by ?ident .
  ?ident crm:P190_has_symbolic_content "3bff80eb8006ef6630a072ae102fe727" .
  ?ident crm:P2_has_type <https://data.getty.edu/local/thesaurus/ref-id> .
  ?hmo crm:P65_shows_visual_item ?image
} limit 1000
>>>
```

For convenience, the pattern sets work well with `lodgatewayclient.LODGatewayClient`s:

```
>>> from lodgatewayclient import LODGatewayClient
>>> l = LODGatewayClient("https://staging-data.jpcarchive.org")
>>> archival.set_sparql_client_method(l.sparql)
>>> collections = archival.run_pattern("list_collections")
>>> collections[0]
{'collection': {'type': 'uri', 'value': 'https://staging-data.jpcarchive.org/component/e3e536ae-84b9-5d80-8eae-97ad774c128e'}}
>>> archival.run_pattern("get_images_for_a_refid")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/bosteen/Workspace/getty-jsonld-sparql-patterns/src/gettysparqlpatterns/ENV/lib/python3.10/site-packages/gettysparqlpatterns/registry.py", line 172, in run_pattern
    raise RequiredParametersMissingError(
gettysparqlpatterns.registry.RequiredParametersMissingError: Query requires the following parameters: ['refid']
>>> images = archival.run_pattern("get_images_for_a_refid", refid="3bff80eb8006ef6630a072ae102fe727")
>>> images[0]
{'image': {'type': 'uri', 'value': 'https://staging-data.jpcarchive.org/media/image/dams:JPC-3bff80eb8006ef6630a072ae102fe727_0006_001'}}
>>> lacounts = SPARQLRegistry.get_patternsets("la_counts")
>>> lacounts.set_sparql_client_method(l.sparql)
>>> lacounts.list_patterns()
['count_informationobjects', 'count_groups', 'count_persons', 'count_hmos', 'count_visualitems']
>>> lacounts.run_pattern("count_groups")
'338'
>>> getty = LODGatewayClient("https://data.getty.edu/research/collections")
>>> lacounts.run_pattern("count_groups", getty.sparql)
'982'
>>>
```