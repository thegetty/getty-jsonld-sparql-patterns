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
        "description": "List all the published collections (top-level records)",
        "sparql_pattern": """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT * WHERE {
  GRAPH ?collection {
  ?collection <http://www.cidoc-crm.org/cidoc-crm/P2_has_type> <http://vocab.getty.edu/aat/300375748> .
  }
} LIMIT 1000""",
        "stype": "select",
    },
]
