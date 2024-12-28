"""Examples demonstrating tree node styling capabilities."""
from typing import Dict

from rich.style import Style as RichStyle

from src.tree_interval import Leaf, Position, Tree
from src.tree_interval.rich_printer import RichPrintConfig, RichTreePrinter


def example_syntax_highlighting():
    """Demonstrates syntax-highlighting style tree visualization."""
    tree = Tree("AST Example")

    # Create nodes with different types
    root = Leaf(Position(0, 100), info={"type": "Module", "name": "main"})
    func_def = Leaf(Position(10, 90),
                    info={
                        "type": "FunctionDef",
                        "name": "process_data"
                    })
    args = Leaf(Position(20, 30), info={"type": "Arguments"})

    # Build tree structure
    tree.root = root
    tree.add_leaf(func_def)
    func_def.add_child(args)

    # Apply syntax highlighting styles
    def apply_syntax_styles(node: Leaf) -> None:
        """Apply syntax highlighting based on node type."""
        if isinstance(node.info, Dict):
            node_type = node.info.get('type', '')
            if node_type == 'Module':
                node.rich_style = RichStyle(color="green", bold=True)
            elif node_type == 'FunctionDef':
                node.rich_style = RichStyle(color="blue", bold=False)
            elif node_type == 'Arguments':
                node.rich_style = RichStyle(color="yellow", bold=False)

    # Apply styles to all nodes
    for node in tree.flatten():
        apply_syntax_styles(node)

    # Print with rich formatting
    printer = RichTreePrinter(RichPrintConfig(show_position=True))
    print("\nSyntax Highlighted Tree:")
    printer.print_tree(tree)


def example_selected_node():
    """Demonstrates highlighting selected nodes."""
    tree = Tree("Selection Example")
    root = Leaf(Position(0, 100), info="Root")
    child1 = Leaf(Position(10, 40), info="Selected Node")
    child2 = Leaf(Position(50, 90), info="Normal Node")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    # Mark node as selected
    child1.selected = True
    child1.rich_style = RichStyle(color="red", bold=True)

    printer = RichTreePrinter()
    print("\nTree with Selected Node:")
    printer.print_tree(tree)


if __name__ == "__main__":
    print("=== Tree Styling Examples ===")
    example_syntax_highlighting()
    example_selected_node()
