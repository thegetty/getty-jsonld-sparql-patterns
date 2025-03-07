patternlist = [
    {
        "name": "count_informationobjects",
        "description": "",
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT (count(distinct ?inf) as ?count) WHERE {
  GRAPH ?inf {
    ?inf <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> crm:E73_Information_Object .
  } 
} LIMIT 1""",
        "stype": "count",
    },
    {
        "name": "count_groups",
        "description": "",
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT (count(distinct ?inf) as ?count) WHERE {
  GRAPH ?inf {
    ?inf <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> crm:E74_Group .
  } 
} LIMIT 1""",
        "stype": "count",
    },
    {
        "name": "count_persons",
        "description": "",
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT (count(distinct ?inf) as ?count) WHERE {
  GRAPH ?inf {
    ?inf <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> crm:E21_Person .
  } 
} LIMIT 1""",
        "stype": "count",
    },
    {
        "name": "count_hmos",
        "description": "",
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT (count(distinct ?inf) as ?count) WHERE {
  GRAPH ?inf {
    ?linkinf <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> crm:E73_Information_Object .
    ?inf crm:P46i_forms_part_of ?linkinf .
  } 
} LIMIT 1""",
        "stype": "count",
    },
    {
        "name": "count_visualitems",
        "description": "",
        "sparql_pattern": """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT (count(distinct ?inf) as ?count) WHERE {
  GRAPH ?inf {
    ?inf <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> crm:E36_Visual_Item .
  } 
} LIMIT 1""",
        "stype": "count",
    },
]
