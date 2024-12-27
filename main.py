"""
Tree Interval Package Demo - Rich Printer Examples
"""

from src.tree_interval import (
    Leaf,
    Position,
    Tree,
)
from src.tree_interval.rich_printer import RichTreePrinter, RichPrintConfig
from rich.style import Style


def demonstrate_basic_rich_printing():
    """Basic Rich tree printing example."""
    print("\n=== Basic Rich Printing ===")
    tree = Tree("Basic Example")

    root = Leaf(Position(0, 100, {"type": "Module", "name": "example"}))
    child1 = Leaf(Position(10, 40, {"type": "Function", "name": "hello"}))
    child2 = Leaf(Position(50, 90, {"type": "Class", "name": "MyClass"}))

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    printer = RichTreePrinter()
    printer.print_tree(tree)


def demonstrate_custom_config():
    """Rich printing with custom configuration."""
    print("\n=== Custom Rich Printing ===")
    tree = Tree("Custom Style Example")

    root = Leaf(Position(0, 100, {"type": "Program"}))
    child = Leaf(Position(10, 50, {"type": "Variable"}))
    tree.root = root
    tree.add_leaf(child)

    config = RichPrintConfig(
        show_size=True,
        show_info=True,
        root_style=Style(color="magenta", bold=True),
        node_style=Style(color="yellow"),
        leaf_style=Style(color="green"),
    )

    printer = RichTreePrinter(config)
    printer.print_tree(tree)


def demonstrate_ast_rich_printing():
    """AST visualization with Rich printer."""
    print("\n=== AST Rich Printing ===")
    tree = Tree("AST Example")

    root = Leaf(Position(0, 100, {"type": "Module"}))
    func_def = Leaf(Position(10, 90, {"type": "FunctionDef", "name": "example"}))
    args = Leaf(Position(20, 30, {"type": "Arguments"}))
    body = Leaf(Position(40, 80, {"type": "Body"}))

    tree.root = root
    tree.add_leaf(func_def)
    func_def.add_child(args)
    func_def.add_child(body)

    printer = RichTreePrinter(RichPrintConfig(show_position=False))
    printer.print_tree(tree)


if __name__ == "__main__":
    demonstrate_basic_rich_printing()
    demonstrate_custom_config()
    demonstrate_ast_rich_printing()
