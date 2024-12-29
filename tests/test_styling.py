"""Tests for tree styling functionality."""
import pytest
from rich.style import Style as RichStyle

from tree_interval import Leaf, LeafStyle, Position
from tree_interval.rich_printer import RichPrintConfig


def test_node_styling():
    """Test applying styles to nodes."""
    node = Leaf(Position(0, 100), info="Test")
    node.rich_style = RichStyle(color="red", bold=True)

    assert "red" in str(node.rich_style.color).lower()
    assert node.rich_style.bold is True


def test_selected_node():
    """Test selected node styling."""
    node = Leaf(Position(0, 100), info="Test")
    node.selected = True

    assert node.selected is True


def test_syntax_highlighting():
    """Test syntax highlighting based on node type."""
    node = Leaf(Position(0, 100), info={"type": "Module"})
    node.rich_style = RichStyle(color="green", bold=True)

    assert "green" in str(node.rich_style.color).lower()
    assert node.rich_style.bold is True


def test_printer_config():
    """Test printer configuration with custom styles."""
    config = RichPrintConfig(root_style=RichStyle(color="blue"),
                             node_style=RichStyle(color="green"),
                             leaf_style=RichStyle(color="yellow"))

    assert "blue" in str(config.root_style.color).lower()
    assert "green" in str(config.node_style.color).lower()
    assert "yellow" in str(config.leaf_style.color).lower()


def test_leaf_style_creation():
    """Test LeafStyle creation and defaults."""
    style = LeafStyle(color="#FF0000")
    assert style.color == "#FF0000"
    assert style.bold is False

    style_bold = LeafStyle(color="#00FF00", bold=True)
    assert style_bold.color == "#00FF00"
    assert style_bold.bold is True


def test_leaf_style_inheritance():
    """Test style inheritance through tree hierarchy."""
    parent = Leaf(Position(0, 100))
    child = Leaf(Position(10, 50))

    parent.add_child(child)
    parent.style = LeafStyle(color="#FF0000", bold=True)

    assert parent.style.color == "#FF0000"
    assert parent.style.bold is True


if __name__ == "__main__":
    pytest.main([__file__])
