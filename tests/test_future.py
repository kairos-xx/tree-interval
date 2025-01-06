
"""Test Future attribute handling."""
import pytest
from tree_interval.core.future import Future


class _Nested:
    def __init__(self):
        self._dict = {}

    def __getattr__(self, name):
        return Future(name, frame=1, instance=self)

    def __setattr__(self, name, value):
        if name == "_dict":
            super().__setattr__(name, value)
        else:
            self._dict[name] = value

    def __getstate__(self):
        return self._dict

    def __setstate__(self, state):
        self._dict = state


@pytest.fixture
def nested():
    return _Nested()


def test_future_attribute_creation(nested):
    """Test that Future creates new attributes properly"""
    instance = nested
    instance.test = _Nested()
    instance.test.sub = 42
    assert hasattr(instance, "test")
    assert hasattr(instance.test, "sub")
    assert instance.test.sub == 42


def test_future_nested_creation(nested):
    """Test nested attribute creation"""
    instance = nested
    instance.a = _Nested()
    instance.a.b = _Nested()
    instance.a.b.c = _Nested()
    instance.a.b.c.d = 123
    assert hasattr(instance, "a")
    assert hasattr(instance.a, "b") 
    assert hasattr(instance.a.b, "c")
    assert hasattr(instance.a.b.c, "d")
    assert instance.a.b.c.d == 123
