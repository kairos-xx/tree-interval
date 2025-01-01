
import pytest
from tree_interval.core.future import Future
from tree_interval.core.frame_analyzer import FrameAnalyzer

class TestNested:
    def __init__(self) -> None:
        self.__dict__ = {}

    def __getattr__(self, name: str):
        return Future(name, frame=1, instance=self, new_return=type(self)())

def test_future_attribute_creation():
    """Test that Future creates new attributes properly"""
    instance = TestNested()
    # This should create the attribute 'test' on instance
    instance.test.sub = 42
    assert hasattr(instance, 'test')
    assert hasattr(instance.test, 'sub')
    assert instance.test.sub == 42

def test_future_attribute_error():
    """Test that Future raises AttributeError for non-existent attributes"""
    instance = TestNested()
    with pytest.raises(AttributeError) as exc_info:
        # Accessing a non-existent attribute should raise
        _ = instance.does_not_exist.value
    assert "not found" in str(exc_info.value)

def test_future_nested_creation():
    """Test nested attribute creation"""
    instance = TestNested()
    instance.a.b.c.d = 123
    assert hasattr(instance, 'a')
    assert hasattr(instance.a, 'b')
    assert hasattr(instance.a.b, 'c')
    assert hasattr(instance.a.b.c, 'd')
    assert instance.a.b.c.d == 123

def test_future_frame_analyzer_integration():
    """Test that Future works with FrameAnalyzer"""
    instance = TestNested()
    # This should trigger FrameAnalyzer
    with pytest.raises(AttributeError) as exc_info:
        instance.test.missing
    assert "not found" in str(exc_info.value)
