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
      graph ?inf { ?s ?p $URI . }
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
