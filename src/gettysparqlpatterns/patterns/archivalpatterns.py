patternlist = [
    {
        "name": "inf_hmo_not_ready",
        "description": (
            "Given a Linked Art HumanMadeObject or a InformationObject URI, "
            "run an ASK query to see if it is for preview only and not intended for production."
        ),
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
ASK {
  {
  <$URI> crm:P2_has_type <https://data.getty.edu/local/thesaurus/aspace-finding-aid-status/notreadyforproduction> .
  } UNION {
  ?inf crm:P2_has_type <https://data.getty.edu/local/thesaurus/aspace-finding-aid-status/notreadyforproduction> .
  <$URI> crm:P46i_forms_part_of ?inf .
  }
} """,
        "stype": "ask",
    },
    {
        "name": "inf_not_ready",
        "description": (
            "Given a Linked Art InformationObject URI run an ASK query to see if it is for preview only and not intended for production."
        ),
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
ASK {
  <$URI> crm:P2_has_type <https://data.getty.edu/local/thesaurus/aspace-finding-aid-status/notreadyforproduction> .
} """,
        "stype": "ask",
    },
    {
        "name": "hmo_not_ready",
        "description": (
            "Given a Linked Art HumanMadeObject URI run an ASK query to see if it is for preview only and not intended for production."
        ),
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
ASK {
  ?inf crm:P2_has_type <https://data.getty.edu/local/thesaurus/aspace-finding-aid-status/notreadyforproduction> .
  <$URI> crm:P46i_forms_part_of ?inf .
} """,
        "stype": "ask",
    },
    {
        "name": "hmo_not_ready",
        "description": (
            "Given a Linked Art HumanMadeObject URI run an ASK query to see if it is for preview only and not intended for production."
        ),
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
ASK {
  ?inf crm:P2_has_type <https://data.getty.edu/local/thesaurus/aspace-finding-aid-status/notreadyforproduction> .
  <$URI> crm:P46i_forms_part_of ?inf .
} """,
        "stype": "ask",
    },
    {
        "name": "is_part_of_production",
        "description": "Tests to see if the given URI is the 'object' of any triple in an InformationObject named graph where the InformationObject is not marked as not ready for production",
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
ASK {
      ?inf a crm:E73_Information_Object .
      graph ?inf { ?s ?p <$URI> . }
      filter NOT EXISTS {
    ?inf crm:P2_has_type <https://data.getty.edu/local/thesaurus/aspace-finding-aid-status/notreadyforproduction> .
  }
}""",
        "stype": "ask",
    },
    {
        "name": "hmo_has_component",
        "description": "",
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
ASK {
  <$URI> crm:P46i_forms_part_of ?inf .
} """,
        "stype": "ask",
    },
    {
        "name": "hmo_list_components",
        "description": "",
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT ?inf WHERE {
  <$URI> crm:P46i_forms_part_of ?inf .
} """,
        "stype": "select",
    },
    {
        "name": "list_collections",
        "description": "List all the published collections (top-level records) with accession numbers",
        "sparql_pattern": """
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT ?component ?eadid WHERE {
  ?component ?idby ?foo .
  ?foo crm:P2_has_type <https://data.getty.edu/local/thesaurus/ead-id> .
  ?foo crm:P190_has_symbolic_content ?eadid .
} LIMIT $LIMIT""",
        "stype": "select",
        "default_values": {"LIMIT": "800"},
    },
    {
        "name": "list_collections_w_findingaidstatus",
        "description": "List all the published collections (top-level records) with their accession number, finding aid status, and title. Multiple titles will created multiple rows. Default LIMIT parameter is set to 100.",
        "sparql_pattern": """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT ?accession ?inf ?findaidclass ?findaidclassname ?title WHERE {
  ?inf ?idby ?cl .
  ?inf rdfs:label ?title .
  ?cl crm:P2_has_type <https://data.getty.edu/local/thesaurus/ead-id> .
  ?cl crm:P190_has_symbolic_content ?accession .
  ?inf crm:P94i_was_created_by ?creby .
  ?creby crm:P2_has_type ?findaidclass .
  ?findaidclass rdfs:label ?findaidclassname .
} LIMIT $LIMIT""",
        "stype": "select",
        "default_values": {"LIMIT": "100"},
    },
    {
        "name": "get_collection_uri_with_accession_number",
        "description": "Given an accession number (ACCESSION), this query will find the matching component URI for the collection.",
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX aat: <http://vocab.getty.edu/aat/>

SELECT ?informationobject WHERE { GRAPH ?informationobject {
    ?inf crm:P190_has_symbolic_content "$ACCESSION" .
    ?inf crm:P2_has_type aat:300312355 .
  }
}""",
        "stype": "select",
    },
]
