import pytest

from tree_interval import (
    Leaf,
    Position,
    Tree,
    TreeVisualizer,
    VisualizationConfig,
)


def test_visualizer_empty_tree(capsys):
    tree = Tree("Test")
    TreeVisualizer.visualize(tree)
    captured = capsys.readouterr()
    assert "Empty tree" in captured.out


def test_visualizer_position_formats():
    tree = Tree("Test")
    root = Leaf(Position(0, 100), info="Root")
    tree.root = root

    config = VisualizationConfig(position_format="position")
    TreeVisualizer.visualize(tree, config)

    config.position_format = "tuple"
    TreeVisualizer.visualize(tree, config)


def test_visualizer_node_formatting():
    tree = Tree("Test")
    root = Leaf(Position(0, 100), info={"type": "Module"})
    child = Leaf(Position(10, 50), info={"type": "Function"})
    tree.root = root
    root.add_child(child)

    config = VisualizationConfig(show_info=True, show_size=True)
    TreeVisualizer.visualize(tree, config)


def test_empty_tree_visualization():
    tree = Tree("")
    TreeVisualizer.visualize(tree)
    assert True  # Verify no exceptions


def test_custom_style_visualization():
    from tree_interval import LeafStyle

    tree = Tree("")
    node = Leaf(Position(0, 100))
    node.style = LeafStyle(color="#FF0000", bold=True)
    tree.root = node
    TreeVisualizer.visualize(tree)
    assert True


def test_node_info_truncation():
    tree = Tree("")
    node = Leaf(Position(0, 100), info="x" * 1000)  # Very long info
    tree.root = node
    TreeVisualizer.visualize(tree)
    assert True


def test_terminal_width_fallback_monkey(monkeypatch):
    """Test terminal width fallback when get_terminal_size fails."""
    from tree_interval.visualizer.config import get_terminal_width

    def mock_get_terminal_size():
        raise OSError("Terminal size not available")

    monkeypatch.setattr("shutil.get_terminal_size", mock_get_terminal_size)
    width = get_terminal_width()
    assert width == 80  # Check fallback value


def test_terminal_width_fallback_attribute_error(monkeypatch):
    """Test terminal width fallback when terminal size has no columns."""
    from tree_interval.visualizer.config import get_terminal_width

    def mock_get_terminal_size():
        class MockSize:
            pass

        return MockSize()  # No columns attribute

    monkeypatch.setattr("shutil.get_terminal_size", mock_get_terminal_size)
    width = get_terminal_width()
    assert width == 80  # Check fallback value


def test_show_children_count():
    """Test visualization with children count display enabled."""
    tree = Tree("Test")
    root = Leaf(Position(0, 100))
    child1 = Leaf(Position(10, 50))
    child2 = Leaf(Position(60, 90))
    tree.root = root
    root.add_child(child1)
    root.add_child(child2)

    config = VisualizationConfig(show_children_count=True)
    TreeVisualizer.visualize(tree, config)
    assert len(root.children) == 2


def test_terminal_width_fallback():
    """Test terminal width fallback value."""
    from shutil import get_terminal_size

    from tree_interval.rich_printer.config import get_terminal_width

    def mock_get_terminal_size():
        raise Exception("Terminal size not available")

    old_get_terminal_size = get_terminal_size
    get_terminal_size = mock_get_terminal_size
    width = get_terminal_width()
    assert width == 80
    get_terminal_size = old_get_terminal_size


def test_terminal_width_success(monkeypatch):
    """Test successful terminal width retrieval."""
    from collections import namedtuple

    from tree_interval.visualizer.config import get_terminal_width

    MockSize = namedtuple("MockSize", ["columns"])
    mock_size = MockSize(columns=100)

    def mock_get_terminal_size():
        return mock_size

    monkeypatch.setattr("shutil.get_terminal_size", mock_get_terminal_size)
    width = get_terminal_width()
    assert width == 100


if __name__ == "__main__":
    pytest.main([__file__])
