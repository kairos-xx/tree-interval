"""Rich printer examples demonstrating various features."""

from rich.style import Style

from src.tree_interval import Leaf, Position, Tree
from src.tree_interval.rich_printer import RichPrintConfig, RichTreePrinter
from src.tree_interval.visualizer import TreeVisualizer, VisualizationConfig


def example_basic():
    """Basic tree printing example."""
    tree = Tree("Basic")
    root = Leaf(Position(0, 100), "Root Node")
    child1 = Leaf(Position(10, 40), "First Child")
    child2 = Leaf(Position(50, 90), "Second Child")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    printer = RichTreePrinter()
    print("\nBasic Tree:")
    printer.print_tree(tree)


def example_custom_styles():
    """Example with custom styling."""
    tree = Tree("Styled")
    root = Leaf(Position(0, 100), {"name": "Main"})
    child = Leaf(Position(10, 50), {"name": "Sub"})

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


def example_custom_visualization():
    """Demonstrate different visualization options."""
    tree = Tree("Visualization Example")
    root = Leaf(Position(0, 100), info="Root")
    child1 = Leaf(Position(10, 40), info="Child 1")
    child2 = Leaf(Position(50, 90), info="Child 2")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    print("\nDefault visualization:")
    tree.visualize()

    print("\nWith position objects:")
    TreeVisualizer.visualize(
        tree,
        VisualizationConfig(position_format="position"),
    )

    print("\nWith tuples and children count:")
    TreeVisualizer.visualize(
        tree,
        VisualizationConfig(
            position_format="tuple", show_children_count=True, show_size=False
        ),
    )


def example_json_serialization():
    """Demonstrate JSON serialization."""
    # Create a simple tree
    tree = Tree("Serialization Example")
    root = Leaf(Position(0, 100), info="Root")
    child = Leaf(Position(10, 50), info="Child")
    tree.root = root
    tree.add_leaf(child)

    # Serialize to JSON
    json_str = tree.to_json()
    print("JSON representation:", json_str)

    # Deserialize from JSON
    loaded_tree = Tree.from_json(json_str)
    print("\nDeserialized tree:")
    loaded_tree.visualize()


def example_ast_tree():
    """Example showing AST-like structure."""
    tree = Tree("AST")
    root = Leaf(Position(0, 100), {"type": "Module"})
    func = Leaf(Position(10, 90), {"type": "FunctionDef", "name": "example"})
    args = Leaf(Position(20, 30), {"type": "Arguments"})

    tree.root = root
    tree.add_leaf(func)
    func.add_child(args)

    config = RichPrintConfig(show_position=False)
    printer = RichTreePrinter(config)
    print("\nAST Tree:")
    printer.print_tree(tree)


def run_demo():
    print("=== Rich Printer Examples ===")
    example_basic()
    example_custom_styles()
    example_custom_visualization()
    example_json_serialization()
    example_ast_tree()


if __name__ == "__main__":
    run_demo()
