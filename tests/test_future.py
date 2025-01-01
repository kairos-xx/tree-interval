import pytest

from tree_interval.core.future import Future


class _Nested:

    def __init__(self) -> None:
        self.__dict__ = {}

    def __getattr__(self, name: str):
        return Future(name, frame=1, instance=self, new_return=type(self)())


@pytest.fixture
def nested():
    return _Nested()


def test_future_attribute_creation(nested):
    """Test that Future creates new attributes properly"""
    instance = nested
    instance.test.sub = 42  # pyright: ignore
    assert hasattr(instance, 'test')
    assert hasattr(instance.test, 'sub')
    assert instance.test.sub == 42  # pyright: ignore


def test_future_nested_creation(nested):
    """Test nested attribute creation"""
    instance = nested
    instance.a.b.c.d = 123
    assert hasattr(instance, 'a')
    assert hasattr(instance.a, 'b')
    assert hasattr(instance.a.b, 'c')  # pyright: ignore
    assert hasattr(instance.a.b.c, 'd')  # pyright: ignore
    assert instance.a.b.c.d == 123  # pyright: ignore


def test_future_frame_analyzer_integration(nested):
    """Test that Future works with FrameAnalyzer"""
    instance = nested
    with pytest.raises(AttributeError) as exc_info:
        _ = instance.test.missing  # pyright: ignore
        assert "not found" in str(exc_info.value)
