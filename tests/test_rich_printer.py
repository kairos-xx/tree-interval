"""Tests for Rich tree printer."""

import pytest
from rich.console import Console
from rich.style import Style

from src.tree_interval import Leaf, Position, Tree
from src.tree_interval.rich_printer import RichPrintConfig, RichTreePrinter


@pytest.fixture
def basic_tree():
    """Fixture for creating a basic test tree."""
    tree = Tree("Test")
    root = Leaf(Position(0, 100), "Root")
    child = Leaf(Position(10, 50), "Child")
    tree.root = root
    tree.add_leaf(child)
    return tree


@pytest.fixture
def empty_tree():
    """Fixture for creating an empty tree."""
    return Tree("Test")


@pytest.fixture
def console():
    """Fixture for creating a Rich console."""
    return Console(record=True)


def test_rich_printer_empty_tree(empty_tree, console):
    """Test printing an empty tree."""
    printer = RichTreePrinter(console=console)

    with console.capture() as capture:
        printer.print_tree(empty_tree)
    output = capture.get()
    assert "Empty tree" in output


def test_rich_printer_basic_tree(basic_tree, console):
    """Test printing a basic tree structure."""
    printer = RichTreePrinter(console=console)

    with console.capture() as capture:
        printer.print_tree(basic_tree)
    output = capture.get()
    assert "[0-100]" in output


def test_rich_printer_custom_config(basic_tree, console):
    """Test printing with custom configuration."""
    config = RichPrintConfig(show_size=False, show_info=False)
    printer = RichTreePrinter(config)

    with console.capture() as capture:
        printer.print_tree(basic_tree)

    output = capture.get()
    assert "size=" not in output
    assert "info=" not in output


def test_rich_printer_custom_styles(basic_tree, console):
    """Test printing with custom styles."""
    config = RichPrintConfig(
        root_style=Style(color="red", bold=True),
        node_style=Style(color="blue"),
        leaf_style=Style(color="green"),
    )
    printer = RichTreePrinter(config, console=console)

    with console.capture() as capture:
        printer.print_tree(basic_tree)
    output = capture.get()
    assert output.strip() != ""


if __name__ == "__main__":
    pytest.main([__file__])
