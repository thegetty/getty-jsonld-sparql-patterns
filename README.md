# Getty SPARQL Patterns
A python library of SPARQL queries for use with the published data structures and ontologies in use at the Getty and held in public SPARQLable endpoints.

## Example Usage:

### SPARQLRegistry

The key class is the `SPARQLRegistry`:

```
Python 3.10.5 (v3.10.5:f377153967, Jun  6 2022, 12:36:10) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from gettysparqlpatterns import SPARQLRegistry
```

This class can be used directly, and contains references to all the pattern sets within this module. The methods `browse_patternsets` and `list_patternsets` can be used to see the top-level groupings and what sort of SPARQL patterns they hold:

```
>>> SPARQLRegistry.browse_patternsets()
[('archival', <gettysparqlpatterns.registry.PatternSet object at 0x110228280>, 'A set of patterns to explore different connections between resources in the Getty archival dataset')]
>>> SPARQLRegistry.list_pattern_names()
['archival']
```

NB Only one patternset is pre-loaded currently, and in future the `SPARQLRegistry` might not preemptively load any patternset without request.

#### list available patternsets

This package ships with a few patternsets that can be loaded and registered as desired. To see the list of built in patternsets:

```
>>> SPARQLRegistry.list_available_patternset_presets()
['archival_patterns.json', 'la_counts.json', 'linked_art_filters.json']
```

To load a patternset from these:

```
>>> # Either load it as part of the registered sets
>>> SPARQLRegistry.load_from_preset('linked_art_counts', 'la_counts.json')
<gettysparqlpatterns.registry.PatternSet object at 0x10d94e290>
>>> SPARQLRegistry.list_pattern_names()
['archival', 'linked_art_counts']

>>> # Or, load it as a standalone pattern set:
>>> p = PatternSet(from_builtin="la_counts.json")
>>> p.name, p.description
('Counting numbers of Linked Art objects', 'A set of SPARQL patterns for counting how many resources of certain types are known to the SPARQL endpoint.')
>>> # NB This does not add the PatternSet to the registry:
>>> SPARQLRegistry.list_pattern_names()
['archival']

>>> # A PatternSet can be registered with a name so that any function can find and use it:
>>> SPARQLRegistry.register("linked_art_counts", p)
>>> SPARQLRegistry.list_pattern_names()
['archival', 'linked_art_counts']
```

To remove a registered pattern set from the SPARQLRegistry:

```
>>> SPARQLRegistry.register("linked_art_counts", p)

...

>>> SPARQLRegistry.remove_patternset("linked_art_counts")
>>> SPARQLRegistry.list_pattern_names()
['archival']
```

#### Why register pattern sets?

When a PatternSet is loaded, the SPARQL patterns are loaded, parsed and held as `string.Template` objects. The data in the object is immutable (aside from the sparql_client_method attribute), and so can be freely used with multiple threads and persisted. It also allows for encapsulated functions to reuse previously retrieved and loaded data, which may come from an HTTP endpoint.


### PatternSet usage

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

```

The list_patterns method can be filtered in the same manner:
```
>>> archival.list_patterns("select")
['hmo_list_components', 'list_collections', 'get_images_for_a_refid']
```

More information can be found for both the pattern set and also each SPARQL pattern, if the author has added additional information:

```
>>> archival.list_patterns()
['inf_hmo_not_ready', 'inf_not_ready', 'hmo_not_ready', 'hmo_has_component', 'hmo_list_components', 'list_collections', 'get_images_for_a_refid']

>>> archival.description
'A set of SPARQL patterns for getting specific bits of information from Getty-published\n    archival metadata held in Linked Data.'

# and for an individual pattern:
>>> infhmonotready = archival.get_pattern("inf_hmo_not_ready")
>>> infhmonotready.description
'Given a Linked Art HumanMadeObject or a InformationObject URI, run an ASK query to see if it is for preview only and not intended for production.'

# The 'stype' is the type of SPARQL query it corresponds to: ask, select, construct and count.
>>> infhmonotready.stype
'ask'
>>>
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

For convenience, the pattern sets work well with `lodgatewayclient.LODGatewayClient` instances:

```
>>> from lodgatewayclient import LODGatewayClient
>>> l = LODGatewayClient("https://data.jpcarchive.org")

# "use_lodgateway_for_queries" to set the sparql client:
>>> archival.use_lodgateway_for_queries(l)

# Or set the default method to use for sparql queries directly:
# This expects a function that operates like the `LODGatewayClient.sparql()` function
>>> archival.set_sparql_client_method(l.sparql)


# NB if no SPARQL function is set, run_pattern() will raise a NoSPARQLEndpointSetError

>>> collections = archival.run_pattern("list_collections")
>>> collections[0]
{'collection': SPARQLURI(URI <'https://data.getty.edu/research/collections/component/c7703138-d4a4-5e24-b8a2-117f0882cf8c'>)}

>>> raw_sparql_response = l.sparql(archival.get_pattern("list_collections"))
>>> raw_sparql_response


# See later about SPARQLURI and SPARQLLiteral in the responses
```

Some patterns require parameters. This is seen in the `.keyword_parameters` attribute for a given pattern, and is listed in the browse view for a pattern set.

```
>>> archival.run_pattern("get_images_for_a_refid")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/bosteen/Workspace/getty-jsonld-sparql-patterns/src/gettysparqlpatterns/ENV/lib/python3.10/site-packages/gettysparqlpatterns/registry.py", line 172, in run_pattern
    raise RequiredParametersMissingError(
gettysparqlpatterns.registry.RequiredParametersMissingError: Query requires the following parameters: ['refid']
```

Parameters can be passed in as keyword parameters to the `run_pattern` method. This method will attempt to render the base SPARQL response into a simpler form, depending on the type of pattern.

```
>>> images = archival.run_pattern("get_images_for_a_refid", refid="3bff80eb8006ef6630a072ae102fe727")
>>> images[0]
{'image': SPARQLURI(URI <'https://data.jpcarchive.org/media/image/dams:JPC-3bff80eb8006ef6630a072ae102fe727_0001_001'>)}
>>> print(f"First image URI found from the responses: {images[0]['image']}")
First image URI found from the responses: https://data.jpcarchive.org/media/image/dams:JPC-3bff80eb8006ef6630a072ae102fe727_0001_001
```

#### `default_values` for parameters

SPARQL templates may provide parameters (such as a LIMIT or SERVICE) where it may be useful to provide a default value. If a pattern has any default parameters, they will be in the `.default_values` attribute. Any parameter passed to a run or format method will override any default value of the same name.

#### Adding SPARQL Patterns to a PatternSet

Patterns can be added to (or updated in) a PatternSet using the 'add_pattern' method, supplying the parameters needed to configure it correctly. If a pattern is added using the same 'name' as an existing one, the new pattern will overwrite the old one.

The method takes the following parameters:

```
add_pattern(
    name: str, 
    sparql_pattern: str, 
    stype: Literal['ask', 'select', 'construct', 'count'], 
    description: str | None = None, 
    default_values: dict | None = None, 
    applies_to: list | None = None, 
    ask_filter: bool | None = None
    )
```

Mandatory:
- 'name'
  - the name or label for the pattern. Used to reference it within the PatternSet
- 'sparql_pattern'
  - The 'string.Template' formatted SPARQL pattern. See https://docs.python.org/3/library/string.html#template-strings for more information. 'string.Template' was used to avoid having to escape every use of '{}' characters, which are common in SPARQL.
- 'stype'. Affects how the 'run' function interprets the response from the SPARQL engine.
  - 'select' - Expects a set of rows, which will be turned into a list of rows, expressed as 'dict' objects.
  - 'construct' - Expects some sort of response which should not be interpreted as a query response, and will be returned unchanged to the client.
  - 'ask' - will return 'true' or 'false'
  - 'count' - Special case of a 'select' query that will contain a '?count' variable that should be cast as an integer as its return value.

(There are more details on these types further on in this README).

Optional:
- 'description' - Description of the aim of this SPARQL pattern as documentation.
- 'default_values' - a dict of default values to use in the template, if none are provided by the user. For example, the pattern may provide 'LIMIT $LIMIT' to allow for a custom number of rows to be returned. Setting 'default_values' to `{"LIMIT": "10"}` would ensure that it would default to 10 otherwise.
- 'applies_to' - List of types that the SPARQL filter it targeted for. This is primarily used to help filtering or selecting useful patterns to use, and the PatternSet list/browse functions accept a parameter `by_applies_to` which can be used to show only exact matches.
- 'ask_filter' - a boolean that indicates whether a SPARQL ASK response was 'successful' or not. This depends on the query and the business logic of the intent, as a 'success' could mean that the ASK is False for a given URI.

### `run_pattern` SPARQL query type responses

While the pattern set can be used to format SPARQL queries, the `run_pattern` method interprets the SPARQL response based on the type of query.

- `ask` will return a (python) boolean response, rather than a raw SPARQL JSON body.
- `select` will return a list of results, each variable will have the standard SPARQL 1.1 response format
- `count` is a specific version of a select query, that expects a `count` variable in the response. This will return the numeric value of this variable
- `construct` will return the SPARQL 1.1 response verbatim as a string, rather than attempt to parse it into an RDF object of some kind. 

#### ASK
```
# ASK
>>> archival.get_pattern("hmo_not_ready").stype
'ask'
>>> archival.get_pattern("hmo_not_ready").keyword_parameters
['URI']
>>> archival.run_pattern("hmo_not_ready", URI="https://data.getty.edu/ ....")
False
```

#### SELECT (SPARQLURI and SPARQLLiteral)

`SPARQLURI` and `SPARQLLiteral` are subclasses of the class `str` and for all intents and purposes can be used as such, including comparisons, assignments, and being turned into JSON (eg `json.dumps(images)` works as expected.)

However, these are typed as URI or Literal instead of plain `str` and can be distinguished either by querying their `type`, or by looking at the attribute `sparql_type` which will be either 'URI' or 'Literal'.

All values with a 'datatype' of 'http://www.w3.org/2001/XMLSchema#integer' will be cast as an python `int`. Other datatyped Literals will be cast as `SPARQLLiteral`, with the datatype present as a `.datatype` attribute. (No attempt to reduce a datetime to a python `datetime.datetime` object is made at this point.)

```
# SELECT
>>> from lodgatewayclient import LODGatewayClient
>>> getty = LODGatewayClient("https://data.getty.edu/research/collections")
>>> from gettysparqlpatterns import *
>>> archival = SPARQLRegistry.get_patternsets("archival")
>>> archival.set_sparql_client_method(getty.sparql)

>>> collections = archival.run_pattern("list_collections")
>>> collections[0]
{'collection': SPARQLURI(URI <'https://data.getty.edu/research/collections/component/c7703138-d4a4-5e24-b8a2-117f0882cf8c'>)}

>>> collections[0]['collection'].sparql_type
'URI'

# export the first three collections (only three for brevity's sake)
>>> import json
>>> print(json.dumps(collections[:3], indent=2))
[
  {
    "collection": "https://data.getty.edu/research/collections/component/c7703138-d4a4-5e24-b8a2-117f0882cf8c"
  },
  {
    "collection": "https://data.getty.edu/research/collections/component/786224ef-ae38-56cd-915f-f7fdba807dbb"
  },
  {
    "collection": "https://data.getty.edu/research/collections/component/d3f8a16e-817c-5d5f-9519-faff3f6b799a"
  }
]
```

#### COUNT

The 'count' pattern is a convenient form of the SELECT query, which looks for a specifically named 'count' variable in the responses and returns only that numerical value:

```
# COUNT
>>> lacounts.get_pattern("count_groups").stype
'count'
>>> lacounts.run_pattern("count_groups")
338
```

Alternate SPARQL endpoints can be passed as part of the `run_pattern` method call as well:

```
>>> getty = LODGatewayClient("https://data.getty.edu/research/collections")
>>> lacounts.run_pattern("count_groups", getty.sparql)
982
>>>
```

### Create PatternSets programmatically

The classes in this module can be used programmatically to create pattern sets, with export and import options.

```
# Get a suitable SPARQL endpoint for testing:
>>> from lodgatewayclient import LODGatewayClient
>>> getty = LODGatewayClient("https://data.getty.edu/research/collections")


>>> from gettysparqlpatterns import *
>>> test = PatternSet("test patternset")
>>> test.set_sparql_client_method(getty.sparql)

# add a pattern called "Find_a_time_datatype", with an stype of 'select'. Note that the 
# following omits the optional 'description' parameter which can be used to add more documentation
>>> test.add_pattern("Find_a_datatype", """PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
...
... SELECT ?graph ?subject ?predicate ?object
... WHERE {
...   GRAPH ?graph {
...     ?subject ?predicate ?object .
...     FILTER(datatype(?object) = xsd:dateTime)
...   }
... } LIMIT 1""", stype="select")

# Test run it:
>>> test.run_pattern("Find_a_time_datatype")
[{'subject': SPARQLURI(URI <'https://data.getty.edu/research/collections/component/d3f8a16e-817c-5d5f-9519-faff3f6b799a/creation'>), 'predicate': SPARQLURI(URI <'http://www.cidoc-crm.org/cidoc-crm/P82a_begin_of_the_begin'>), 'object': SPARQLLiteral("'2012-01-01T00:00:00.000Z'"), 'graph': SPARQLURI(URI <'https://data.getty.edu/research/collections/component/d3f8a16e-817c-5d5f-9519-faff3f6b799a'>)}]


>>> quad = test.run_pattern("Find_a_datatype")[0]
>>> quad['object'].datatype
'http://www.w3.org/2001/XMLSchema#dateTime'
>>> quad['object'].sparql_type
'Literal'
```

#### Exporting and Importing sets of SPARQL patterns

The patterns can be exported and imported as simple JSON-encodable data, and `PatternSet` instances can hold patterns from multiple sources (however, the patterns have to be named uniquely, or later added patterns will overwrite existing ones).

The creation of new patterns will require some trial and error, so it is expected that a PatternSet would be created in parts, and eventually exported to record the progress made and potentially to include in this module.

NB The reason why the `data/archival_patterns.json` and the `la_count` (Linked Art Count) patterns are initialized differently is to show the two ways that the patterns could be encoded - one as JSON (SPARQL patterns on a single line with \n codes), and the other as a python data structure (which allows for multiline strings which are clearer to read).

```
# Export
>>> exported = test.export_patterns()
>>>
>>> exported
[{'name': 'Find_a_datatype', 'description': 'No description given', 'sparql_pattern': 'PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\nSELECT ?graph ?subject ?predicate ?object\nWHERE {\n  GRAPH ?graph {\n    ?subject ?predicate ?object .\n    FILTER(datatype(?object) = xsd:dateTime)\n  }\n} LIMIT 1', 'stype': 'select'}]

# Import
>>> newtest = PatternSet('new test')
>>> newtest.import_patterns(exported)
>>> newtest.list_patterns()
['Find_a_datatype']

# Import additional patterns without clearing the existing ones:
>>> lacounts = SPARQLRegistry.get_patternsets("la_counts")
>>> newtest.import_patterns(lacounts.export_patterns(), add_to_existing=True)
>>> newtest.list_patterns()
['Find_a_datatype', 'count_informationobjects', 'count_groups', 'count_persons', 'count_hmos', 'count_visualitems']
>>>
```

The PatternSet can also be loaded from a remote JSON resource:

```
>>> ps = PatternSet(from_url="https://gist.githubusercontent.com/benosteen/1253ebccd3bde327a62da9bb5f43c0c0/raw/7d2fd523213c1d5bca43313911d4a2a36d7dc4f2/test.json")
>>> ps.list_patterns()
['inf_not_ready', 'hmo_not_ready', 'is_part_of_production']
>>>
```

Or from an exported PatternSet that is part of this package:

```
>>> SPARQLRegistry.list_available_patternset_presets()
['archival_patterns.json', 'la_counts.json', 'linked_art_filters.json']
>>> ps = PatternSet(from_builtin="la_counts.json")
>>> ps.list_patterns()
['count_informationobjects', 'count_groups', 'count_persons', 'count_hmos', 'count_visualitems', 'count_hmos_with_nonexistant_visitems', 'count_hmos_with_existing_visitems']
```

Or directly from the exported version of another PatternSet (if loading from another source):

```
>>> export = p.export_patterns()

... store 'export' in some other system, like an LOD Gateway for example

>>> # When needed, 'json.load' the stored data into a variable ('export' in this example:)
>>> ps = PatternSet(from_json=export)
>>> ps.list_patterns()
['inf_not_ready', 'hmo_not_ready', 'is_part_of_production']
```
