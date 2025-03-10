from gettysparqlpatterns import SPARQLResponseObj, SPARQLURI, SPARQLLiteral


def test_sparql_response_obj():
    obj = SPARQLResponseObj("value", "type", "datatype")
    assert isinstance(obj, str)
    assert obj == "value"
    assert obj.sparql_type == "type"
    assert obj.datatype == "datatype"
    assert (
        repr(obj)
        == "SPARQLLiteral(\"'value'\", sparql_type='type', datatype=\"'datatype'\")"
    )

    obj_no_datatype = SPARQLResponseObj("value", "type")
    assert obj_no_datatype.datatype is None
    assert repr(obj_no_datatype) == "SPARQLResponseObj('value', sparql_type='type')"


def test_sparql_uri():
    uri = SPARQLURI("http://example.org")
    assert isinstance(uri, str)
    assert uri == "http://example.org"
    assert uri.sparql_type == "URI"
    assert uri.datatype is None
    assert repr(uri) == "SPARQLURI(URI <'http://example.org'>)"


def test_sparql_literal():
    literal = SPARQLLiteral("value", "datatype")
    assert isinstance(literal, str)
    assert literal == "value"
    assert literal.sparql_type == "Literal"
    assert literal.datatype == "datatype"
    assert repr(literal) == "SPARQLLiteral(\"'value'\", datatype=\"'datatype'\")"

    literal_no_datatype = SPARQLLiteral("value")
    assert literal_no_datatype.datatype is None
    assert repr(literal_no_datatype) == "SPARQLLiteral(\"'value'\")"
