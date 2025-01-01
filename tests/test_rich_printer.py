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
        printer.print_tree(None)  # pyright: ignore


def test_format_node_custom_styles():
    leaf = Leaf(Position(0, 100), info={"type": "Module"})
    printer = RichTreePrinter()
    formatted = printer._format_node(leaf, is_root=True)
    assert formatted != ""


def test_format_empty_tree():
    printer = RichTreePrinter()
    printer.print_tree(Tree(""))
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


def test_long_info_truncation():
    """Test that long info strings are truncated properly."""
    printer = RichTreePrinter(RichPrintConfig(terminal_size=40))
    node = Leaf(Position(0, 100), info={"very_long_key": "x" * 100})
    formatted = printer._format_node(node, level=2)
    assert "info=..." in formatted


def test_node_selected_style():
    """Test that selected nodes use the selected style."""
    printer = RichTreePrinter()
    node = Leaf(Position(0, 100))
    node.selected = True
    formatted = printer._format_node(node)
    assert formatted != ""


def test_node_with_no_style():
    """Test node formatting when no style is specified."""
    printer = RichTreePrinter()
    node = Leaf(Position(0, 100))
    node.rich_style = None
    formatted = printer._format_node(node)
    assert formatted != ""


def test_custom_root_no_children():
    """Test visualization from custom root with no children."""
    tree = Tree("Test")
    leaf = Leaf(Position(0, 50), info="Single")
    tree.root = leaf
    printer = RichTreePrinter()
    printer.print_tree(tree, root=leaf)  # Should not raise any errors
    assert True


def test_node_without_rich_style():
    """Test node formatting when rich_style attribute doesn't exist."""
    printer = RichTreePrinter()
    node = Leaf(Position(0, 100))
    delattr(node, "rich_style")  # Remove rich_style attribute
    formatted = printer._format_node(node)
    assert formatted != ""


def test_empty_info_string():
    """Test node formatting with empty info string."""
    printer = RichTreePrinter()
    node = Leaf(Position(0, 100), info="")
    formatted = printer._format_node(node)
    assert formatted != ""


def test_console_without_record():
    """Test printing with console that doesn't support record."""
    console = Console(record=False)
    printer = RichTreePrinter(console=console)
    tree = Tree("Test")
    root = Leaf(Position(0, 100), "Root")
    tree.root = root
    printer.print_tree(tree)  # Should not raise any errors
    assert True


def test_format_node_long_info():
    """Test formatting node with long info string."""
    config = RichPrintConfig(terminal_size=20)
    printer = RichTreePrinter(config)
    info = {"very_long_key": "very_long_value" * 10}
    node = Leaf(Position(0, 10), info=info)
    formatted = printer._format_node(node)
    assert "info=..." in formatted


def test_format_node_custom_style():
    """Test formatting node with custom style."""
    from rich.style import Style

    printer = RichTreePrinter()
    node = Leaf(Position(0, 10))
    node.rich_style = Style(color="red")
    formatted = printer._format_node(node)
    assert formatted is not None


def test_function_def_style():
    """Test style assignment for FunctionDef nodes."""
    from rich.style import Style

    config = RichPrintConfig()
    printer = RichTreePrinter(config)
    node = Leaf(Position(0, 10))
    node.info = {"type": "FunctionDef"}
    style = printer._get_node_style(node)
    assert style == Style(color="cyan")


def test_default_style_fallback():
    """Test fallback to default node style."""
    from rich.style import Style

    config = RichPrintConfig()
    config.leaf_style = Style(color="green", bold=True)
    printer = RichTreePrinter(config)
    node = Leaf(Position(0, 10))
    node.info = {"type": "UnknownType"}
    style = printer._get_node_style(node)
    assert style == config.root_style


def test_terminal_width_with_exception(monkeypatch):
    """Test terminal width fallback when get_terminal_size raises exception."""
    from tree_interval.rich_printer.config import get_terminal_width

    def mock_get_terminal_size(*_, **__):
        raise OSError("Mock error")

    monkeypatch.setattr("shutil.get_terminal_size", mock_get_terminal_size)
    width = get_terminal_width()
    assert width == 80  # Check fallback value


if __name__ == "__main__":
    pytest.main([__file__])
