import pytest

from gettysparqlpatterns import SPARQLRegistry, PatternSet
from gettysparqlpatterns.exceptions import NoSuchPatternError


def test_builtin_patterns_loaded():
    bp = SPARQLRegistry.list_pattern_names()
    assert len(bp) == 1
    assert "archival" in bp


def test_load_preset_and_remove():
    bp = SPARQLRegistry.list_pattern_names()
    assert len(bp) == 1
    assert "archival" in bp

    SPARQLRegistry.load_from_preset(
        "test", SPARQLRegistry.list_available_patternset_presets()[0]
    )
    newlist = SPARQLRegistry.list_pattern_names()
    assert len(newlist) == 2
    assert "test" in newlist

    SPARQLRegistry.remove_patternset("test")

    bp = SPARQLRegistry.list_pattern_names()
    assert len(bp) == 1
    assert "archival" in bp


@pytest.fixture
def pattern_set():
    return PatternSet(name="TestSet")


def test_register(pattern_set):
    SPARQLRegistry.register("TestSet", pattern_set)
    assert "TestSet" in SPARQLRegistry._registry
    assert SPARQLRegistry._registry["TestSet"] == pattern_set


def test_get_patternsets(pattern_set):
    SPARQLRegistry.register("TestSet", pattern_set)
    ps = SPARQLRegistry.get_patternsets()
    assert "TestSet" in ps
    assert SPARQLRegistry.get_patternset("TestSet") == pattern_set


def test_get_patternset(pattern_set):
    SPARQLRegistry.register("TestSet", pattern_set)
    assert SPARQLRegistry.get_patternset("TestSet") == pattern_set
    with pytest.raises(NoSuchPatternError):
        SPARQLRegistry.get_patternset("UnknownSet")


def test_list_pattern_names(pattern_set):
    SPARQLRegistry.register("TestSet", pattern_set)
    assert "TestSet" in SPARQLRegistry.list_pattern_names()


def test_browse_patternsets(pattern_set):
    SPARQLRegistry.register("TestSet", pattern_set)
    assert (
        "TestSet",
        pattern_set,
        pattern_set.description,
    ) in SPARQLRegistry.browse_patternsets()
