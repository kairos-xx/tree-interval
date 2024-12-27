"""Rich printer examples demonstrating various features."""

from rich.style import Style

from src.tree_interval import Leaf, Position, Tree
from src.tree_interval.rich_printer import RichPrintConfig, RichTreePrinter


def example_basic():
    """Basic tree printing example."""
    tree = Tree("Basic")
    root = Leaf(Position(0, 100, "Root Node"))
    child1 = Leaf(Position(10, 40, "First Child"))
    child2 = Leaf(Position(50, 90, "Second Child"))

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    printer = RichTreePrinter()
    print("\nBasic Tree:")
    printer.print_tree(tree)


def example_custom_styles():
    """Example with custom styling."""
    tree = Tree("Styled")
    root = Leaf(Position(0, 100, {"name": "Main"}))
    child = Leaf(Position(10, 50, {"name": "Sub"}))

    tree.root = root
    tree.add_leaf(child)

    config = RichPrintConfig(
        root_style=Style(color="red", bold=True),
        node_style=Style(color="yellow"),
        show_size=False,
    )

    printer = RichTreePrinter(config)
    print("\nStyled Tree:")
    printer.print_tree(tree)


def example_ast_tree():
    """Example showing AST-like structure."""
    tree = Tree("AST")
    root = Leaf(Position(0, 100, {"type": "Module"}))
    func = Leaf(Position(10, 90, {"type": "FunctionDef", "name": "example"}))
    args = Leaf(Position(20, 30, {"type": "Arguments"}))

    tree.root = root
    tree.add_leaf(func)
    func.add_child(args)

    config = RichPrintConfig(show_position=False)
    printer = RichTreePrinter(config)
    print("\nAST Tree:")
    printer.print_tree(tree)


if __name__ == "__main__":
    print("=== Rich Printer Examples ===")
    example_basic()
    example_custom_styles()
    example_ast_tree()
