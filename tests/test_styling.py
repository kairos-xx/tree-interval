"""Tests for tree styling functionality."""
import pytest
from rich.style import Style as RichStyle

from src.tree_interval import Leaf, Position
from src.tree_interval.rich_printer import RichPrintConfig


def test_node_styling():
    """Test applying styles to nodes."""
    node = Leaf(Position(0, 100), info="Test")
    node.rich_style = RichStyle(color="red", bold=True)

    assert node.rich_style.color == "red"
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

    assert node.rich_style.color == "green"
    assert node.rich_style.bold is True


def test_printer_config():
    """Test printer configuration with custom styles."""
    config = RichPrintConfig(root_style=RichStyle(color="blue"),
                             node_style=RichStyle(color="green"),
                             leaf_style=RichStyle(color="yellow"))

    assert config.root_style.color == "blue"
    assert config.node_style.color == "green"
    assert config.leaf_style.color == "yellow"


if __name__ == "__main__":
    pytest.main([__file__])
