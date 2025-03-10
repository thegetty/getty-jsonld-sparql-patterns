from gettysparqlpatterns import PatternSet
from unittest.mock import Mock


def test_init():
    ps = PatternSet(name="TestSet", description="A test pattern set")
    assert ps.name == "TestSet"
    assert ps.description == "A test pattern set"
    assert ps.sparql_client_method is None
    assert ps._patterns == {}


def test_set_sparql_client_method():
    ps = PatternSet(name="TestSet")
    mock_method = Mock()
    ps.set_sparql_client_method(mock_method)
    assert ps.sparql_client_method == mock_method


def test_add_pattern():
    ps = PatternSet(name="TestSet")
    ps.add_pattern(
        name="TestPattern", sparql_pattern="SELECT * WHERE {}", stype="select"
    )
    assert "TestPattern" in ps._patterns
    assert ps._patterns["TestPattern"].name == "TestPattern"
    assert ps._patterns["TestPattern"].sparql_pattern.template == "SELECT * WHERE {}"
    assert ps._patterns["TestPattern"].stype == "select"


def test_browse_patterns():
    ps = PatternSet(name="TestSet")
    ps.add_pattern(
        name="TestPattern", sparql_pattern="SELECT * WHERE {}", stype="select"
    )
    patterns = ps.browse_patterns()
    assert len(patterns) == 1
    assert patterns[0][0] == "TestPattern"


def test_list_patterns():
    ps = PatternSet(name="TestSet")
    ps.add_pattern(
        name="TestPattern", sparql_pattern="SELECT * WHERE {}", stype="select"
    )
    pattern_names = ps.list_patterns()
    assert pattern_names == ["TestPattern"]


def test_get_pattern():
    ps = PatternSet(name="TestSet")
    ps.add_pattern(
        name="TestPattern", sparql_pattern="SELECT * WHERE {}", stype="select"
    )
    pattern = ps.get_pattern("TestPattern")
    assert pattern.name == "TestPattern"


def test_export_patterns():
    ps = PatternSet(name="TestSet")
    ps.add_pattern(
        name="TestPattern", sparql_pattern="SELECT * WHERE {}", stype="select"
    )
    exported = ps.export_patterns()
    assert len(exported) == 1
    assert exported[0]["name"] == "TestPattern"


def test_import_patterns():
    ps = PatternSet(name="TestSet")
    patterns = [
        {
            "name": "ImportedPattern",
            "description": "An imported pattern",
            "sparql_pattern": "SELECT * WHERE {}",
            "stype": "select",
            "keyword_parameters": [],
        }
    ]
    ps.import_patterns(patterns)
    assert "ImportedPattern" in ps._patterns


def test_format_pattern():
    ps = PatternSet(name="TestSet")
    ps.add_pattern(
        name="TestPattern", sparql_pattern="SELECT * WHERE {}", stype="select"
    )
    query = ps.format_pattern("TestPattern")
    assert query == "SELECT * WHERE {}"


def test_run_pattern():
    ps = PatternSet(name="TestSet")
    mock_method = Mock(return_value={"head": {"vars": []}, "results": {"bindings": []}})
    ps.set_sparql_client_method(mock_method)
    ps.add_pattern(
        name="TestPattern", sparql_pattern="SELECT * WHERE {}", stype="select"
    )
    result = ps.run_pattern("TestPattern")
    assert result == []
    mock_method.assert_called_once_with("SELECT * WHERE {}")
