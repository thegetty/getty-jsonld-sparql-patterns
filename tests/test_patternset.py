from gettysparqlpatterns import PatternSet, NoPatternsFoundError
from gettysparqlpatterns.registry import BasePattern
from unittest.mock import Mock, patch
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

    bad_pattern = {}
    with pytest.raises(NoPatternsFoundError):
        ps.import_patterns(bad_pattern)

    bad_pattern2 = {"blah blah blah"}  # iterable but not a list
    with pytest.raises(NoPatternsFoundError):
        ps.import_patterns(bad_pattern2)

    bad_pattern3 = {"blah blah blah": "fooo"}  # iterable but not a list
    with pytest.raises(NoPatternsFoundError):
        ps.import_patterns(bad_pattern3)

    # make sure that what existed is unaffected
    assert len(ps) == 1
    imp_pattern = ps.get_pattern("ImportedPattern")
    assert "ImportedPattern" == imp_pattern.name


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


@pytest.fixture
def pattern_set():
    ps = PatternSet(name="TestSet")
    ps._patterns = {
        "pattern1": BasePattern(
            name="pattern1",
            description="desc1",
            sparql_pattern="sparql1",
            stype="ask",
            default_values={},
            applies_to=["example"],
        ),
        "pattern2": BasePattern(
            name="pattern2",
            description="desc2",
            sparql_pattern="sparql2",
            stype="select",
            default_values={"LIMIT": "1"},
            applies_to=["example"],
        ),
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


# Test the import from URL method inc adding to existing:
def test_import_patterns_from_url(pattern_set):
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "name": "pattern5",
            "description": "desc5",
            "sparql_pattern": "sparql5",
            "stype": "ask",
            "sparql_client_method": None,
            "default_values": None,
        },
        {
            "name": "pattern6",
            "description": "desc6",
            "sparql_pattern": "sparql6",
            "stype": "select",
            "sparql_client_method": None,
            "default_values": None,
        },
    ]
    with patch("requests.get", return_value=mock_response):
        pattern_set.import_patterns_from_url("http://example.com/patterns")

    # default is overwriting
    assert len(pattern_set) == 2
    assert pattern_set[0].name == "pattern5"
    assert pattern_set[1].name == "pattern6"


def test_import_patterns_from_url_add_to_existing(pattern_set):
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "name": "pattern5",
            "description": "desc5",
            "sparql_pattern": "sparql5",
            "stype": "ask",
            "sparql_client_method": None,
            "default_values": None,
        },
        {
            "name": "pattern6",
            "description": "desc6",
            "sparql_pattern": "sparql6",
            "stype": "select",
            "sparql_client_method": None,
            "default_values": None,
        },
    ]
    with patch("requests.get", return_value=mock_response):
        pattern_set.import_patterns_from_url(
            "http://example.com/patterns", add_to_existing=True
        )
    assert len(pattern_set) == 4
    assert pattern_set[2].name == "pattern5"
    assert pattern_set[3].name == "pattern6"


def test_list_patterns_with_filters(pattern_set):
    # Test list_patterns without filters
    result = pattern_set.list_patterns()
    assert result == ["pattern1", "pattern2"]

    # Test list_patterns with by_type filter
    result = pattern_set.list_patterns(by_type="construct")
    assert result == []

    # Test list_patterns with by_type filter
    result = pattern_set.list_patterns(by_type="select")
    assert result == ["pattern2"]

    result = pattern_set.list_patterns(by_applies_to="example")
    assert result == ["pattern1", "pattern2"]
    # Test list_patterns with by_type filter

    result = pattern_set.list_patterns(by_type="select", by_applies_to="example")
    assert result == ["pattern2"]


def test_browse_patterns_with_filters(pattern_set):
    # Test browse_patterns without filters
    result = pattern_set.browse_patterns()
    assert len(result) == 2
    assert result[0][0] == "pattern1"
    assert result[1][0] == "pattern2"

    # Test browse_patterns with by_type filte
    result = pattern_set.browse_patterns(by_type="construct")
    assert result == []

    # Test browse_patterns with by_type filte
    result = pattern_set.browse_patterns(by_type="select")
    assert len(result) == 1
    assert result[0][0] == "pattern2"

    # Test browse_patterns with by_applies_to filter
    result = pattern_set.browse_patterns(by_applies_to="example")
    assert len(result) == 2
    assert result[0][0] == "pattern1"
    assert result[1][0] == "pattern2"

    # Test browse_patterns with by_applies_to filter
    result = pattern_set.browse_patterns(by_type="select", by_applies_to="example")
    assert len(result) == 1
    assert result[0][0] == "pattern2"
