"""Tests for Rich tree printer."""

import pytest
from rich.console import Console

from src.tree_interval import Leaf, Position, Tree
from src.tree_interval.rich_printer import RichPrintConfig, RichTreePrinter


def test_rich_printer_empty_tree():
    tree = Tree("Test")
    printer = RichTreePrinter()
    console = Console(record=True)

    with console.capture() as capture:
        printer.print_tree(tree)

    output = capture.get()
    assert "Empty tree" in output


def test_rich_printer_basic_tree():
    tree = Tree("Test")
    root = Leaf(Position(0, 100, "Root"))
    child = Leaf(Position(10, 50, "Child"))
    tree.root = root
    tree.add_leaf(child)

    printer = RichTreePrinter()
    console = Console(record=True)

    with console.capture() as capture:
        printer.print_tree(tree)

    output = capture.get()
    assert "[0-100]" in output
    assert "[10-50]" in output


def test_rich_printer_custom_config():
    tree = Tree("Test")
    root = Leaf(Position(0, 100, "Root"))
    tree.root = root

    config = RichPrintConfig(show_size=False, show_info=False)
    printer = RichTreePrinter(config)
    console = Console(record=True)

    with console.capture() as capture:
        printer.print_tree(tree)

    output = capture.get()
    assert "size=" not in output
    assert "info=" not in output
