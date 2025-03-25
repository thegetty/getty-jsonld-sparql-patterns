import pytest
from unittest.mock import Mock

from gettysparqlpatterns import (
    RequiredParametersMissingError,
    NoSPARQLEndpointSetError,
)

from gettysparqlpatterns.registry import BasePattern


# Unit tests
def test_init():
    pattern = BasePattern(
        name="test",
        sparql_pattern="SELECT * WHERE { ?s ?p ?o } LIMIT $LIMIT",
        stype="select",
        description="Test pattern",
        default_values={"LIMIT": 10},
        applies_to=["HumanMadeObject"],
    )
    assert pattern.name == "test"
    assert pattern.description == "Test pattern"
    assert pattern.sparql_pattern.template == "SELECT * WHERE { ?s ?p ?o } LIMIT $LIMIT"
    assert pattern.stype == "select"
    assert pattern.default_values == {"LIMIT": 10}
    assert pattern.applies_to == ["HumanMadeObject"]


# Unit tests
def test_init_applies_to_without_list():
    pattern = BasePattern(
        name="test",
        sparql_pattern="SELECT * WHERE { ?s ?p ?o } LIMIT $LIMIT",
        stype="select",
        description="Test pattern",
        default_values={"LIMIT": 10},
        applies_to="HumanMadeObject",
    )
    assert pattern.name == "test"
    assert pattern.applies_to == ["HumanMadeObject"]


def test_set_pattern():
    pattern = BasePattern(
        name="test",
        sparql_pattern="SELECT * WHERE { ?s ?p ?o }",
        stype="select",
    )
    assert pattern.keyword_parameters == []

    pattern._set_pattern("SELECT * WHERE { ?s ?p $value }")
    assert pattern.keyword_parameters == ["value"]


def test_get_query():
    pattern = BasePattern(
        name="test",
        sparql_pattern="SELECT * WHERE { ?s ?p $value } LIMIT $LIMIT",
        stype="select",
        default_values={"LIMIT": 10},
    )
    query = pattern.get_query(value="test_value")
    assert query == "SELECT * WHERE { ?s ?p test_value } LIMIT 10"

    with pytest.raises(RequiredParametersMissingError):
        pattern.get_query()


def test_run():
    mock_sparql_client_method = Mock(return_value={"results": "mocked_results"})
    pattern = BasePattern(
        name="test",
        sparql_pattern="SELECT * WHERE { ?s ?p $value }",
        stype="select",
        sparql_client_method=mock_sparql_client_method,
    )
    result = pattern.run(value="test_value")
    assert result == {"results": "mocked_results"}

    with pytest.raises(RequiredParametersMissingError):
        result = pattern.run()

    pattern.sparql_client_method = None
    with pytest.raises(NoSPARQLEndpointSetError):
        pattern.run()


def test_run_with_default():
    mock_sparql_client_method = Mock(return_value={"results": "mocked_results"})
    pattern = BasePattern(
        name="test",
        sparql_pattern="SELECT * WHERE { ?s ?p $value } LIMIT $LIMIT",
        stype="select",
        sparql_client_method=mock_sparql_client_method,
        default_values={"LIMIT": "10"},
    )
    result = pattern.run(value="test_value")
    assert result == {"results": "mocked_results"}


if __name__ == "__main__":
    pytest.main()
