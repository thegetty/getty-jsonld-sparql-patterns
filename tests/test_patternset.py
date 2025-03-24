from gettysparqlpatterns import PatternSet
from gettysparqlpatterns.registry import BasePattern
from unittest.mock import Mock
import pytest


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


def test_use_lodgateway_for_queries():
    pattern_set = PatternSet(name="TestSet")
    mock_lodgateway = Mock()
    mock_lodgateway.capabilities = {"JSON-LD": True}
    mock_lodgateway.sparql = Mock()
    pattern_set.use_lodgateway_for_queries(mock_lodgateway)
    assert pattern_set.sparql_client_method == mock_lodgateway.sparql

    mock_lodgateway.capabilities = {"JSON-LD": False}
    with pytest.raises(Exception):
        pattern_set.use_lodgateway_for_queries(mock_lodgateway)


def test_add_pattern():
    pattern_set = PatternSet(name="TestSet")
    pattern_set.add_pattern(
        name="test_pattern",
        sparql_pattern="SELECT * WHERE { ?s ?p ?o } LIMIT $LIMIT",
        stype="select",
        description="Test pattern",
        default_values={"LIMIT": 10},
    )
    assert "test_pattern" in pattern_set._patterns
    pattern = pattern_set.get_pattern("test_pattern")
    assert pattern.name == "test_pattern"
    assert pattern.description == "Test pattern"
    assert pattern.sparql_pattern.template == "SELECT * WHERE { ?s ?p ?o } LIMIT $LIMIT"
    assert pattern.stype == "select"
    assert pattern.default_values == {"LIMIT": 10}
    assert "LIMIT" in pattern.keyword_parameters


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
            "sparql_pattern": "SELECT * WHERE {} LIMIT $test",
            "stype": "select",
            "default_values": {"test": 1},
        }
    ]
    ps.import_patterns(patterns)

    imp_pattern = ps.get_pattern("ImportedPattern")
    assert "ImportedPattern" == imp_pattern.name
    assert "An imported pattern" in imp_pattern.description
    assert "SELECT * WHERE {} LIMIT $test" in imp_pattern.sparql_pattern.template
    assert "test" in imp_pattern.keyword_parameters
    assert imp_pattern.default_values.get("test") == 1


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


# test the list-like functionality:


@pytest.fixture
def pattern_set():
    ps = PatternSet(name="TestSet")
    ps._patterns = {
        "pattern1": BasePattern("pattern1", "desc1", "sparql1", "ask", None, None),
        "pattern2": BasePattern("pattern2", "desc2", "sparql2", "select", None, None),
    }
    return ps


def test_len(pattern_set):
    assert len(pattern_set) == 2


def test_getitem(pattern_set):
    assert pattern_set[0].name == "pattern1"
    assert pattern_set[1].name == "pattern2"


def test_iter(pattern_set):
    patterns = [pattern for pattern in pattern_set]
    assert len(patterns) == 2
    assert patterns[0].name == "pattern1"
    assert patterns[1].name == "pattern2"
