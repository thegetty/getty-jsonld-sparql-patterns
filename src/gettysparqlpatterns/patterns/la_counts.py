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
    {
        "name": "count_hmos_with_nonexistant_visitems",
        "description": "",
        "sparql_pattern": """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/> 
SELECT (count (distinct ?images) as ?count) WHERE {  
  ?hmo crm:P65_shows_visual_item ?images .  
  FILTER NOT EXISTS {  
    SERVICE <$VISITEM_SERVICE> {  
      ?images rdf:type ?visimg .  
    }
  }
} LIMIT 1""",
        "stype": "count",
        "default_values": {
            "VISITEM_SERVICE": "https://data.jpcarchive.org/media/sparql"
        },
    },
    {
        "name": "count_hmos_with_existing_visitems",
        "description": "",
        "sparql_pattern": """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/> 
SELECT (count (distinct ?images) as ?count) WHERE {  
  ?hmo crm:P65_shows_visual_item ?images .  
  FILTER EXISTS {  
    SERVICE <$VISITEM_SERVICE> {  
      ?images rdf:type ?visimg .  
    }
  }
} LIMIT 1""",
        "stype": "count",
        "default_values": {
            "VISITEM_SERVICE": "https://data.jpcarchive.org/media/sparql"
        },
    },
]
