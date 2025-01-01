"""Tests for Rich tree printer."""

import pytest
from rich.console import Console
from rich.style import Style

from tree_interval import Leaf, Position, Tree
from tree_interval.rich_printer import RichPrintConfig, RichTreePrinter


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


def test_custom_root_visualization(basic_tree, console):
    """Test visualization from custom root node."""
    child = basic_tree.root.children[0]
    printer = RichTreePrinter(console=console)

    with console.capture() as capture:
        printer.print_tree(basic_tree, root=child)
    output = capture.get()
    assert "Child" in output
    assert "10-50" in output


def test_rich_printer_empty_config():
    printer = RichTreePrinter()
    with pytest.raises(AttributeError):
        printer.print_tree(None)


def test_format_node_custom_styles():
    leaf = Leaf(Position(0, 100), info={"type": "Module"})
    printer = RichTreePrinter()
    formatted = printer._format_node(leaf, is_root=True)
    assert formatted != ""


def test_format_empty_tree():
    printer = RichTreePrinter()
    printer.print_tree(Tree(""))  # Should just print "Empty tree" without raising
    assert True


def test_node_formatting():
    printer = RichTreePrinter()
    node = Leaf(Position(0, 100), info={"type": "test"})
    formatted = printer._format_node(node, is_root=True)
    assert formatted != ""


def test_style_inheritance():
    from rich.style import Style
    config = RichPrintConfig(root_style=Style(color="red"))
    printer = RichTreePrinter(config)
    node = Leaf(Position(0, 100))
    formatted = printer._format_node(node, is_root=True)
    assert formatted != ""


if __name__ == "__main__":
    pytest.main([__file__])
