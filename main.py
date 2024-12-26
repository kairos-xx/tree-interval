
"""
Example usage of the tree structure implementation.

This module demonstrates various features of the tree structure implementation
including visualization, serialization, and tree traversal.
"""

from inspect import currentframe
from json import dumps, loads

from ast_tree_builder import AstTreeBuilder
from tree_core import Leaf, Position, Tree
from tree_visualizer import TreeVisualizer, VisualizationConfig


def example_all_methods():
    """Demonstrate all available methods in Tree and Leaf classes."""
    print("1. Creating a tree and leaves")
    tree = Tree[str]("Example code", start_lineno=1, indent_size=4)

    # Create leaves with different methods
    root = Leaf(0, 100, "root")
    pos = Position(10, 40, "child1")
    pos.lineno = 1
    pos.end_lineno = 2
    pos.col_offset = 10
    pos.end_col_offset = 40
    child1 = Leaf(pos)
    child2 = Leaf((50, 90, "child2"))  # Using tuple

    print("\n2. Building tree structure")
    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    # Create and add grandchildren
    grandchild1 = Leaf(15, 25, "grandchild1")
    grandchild2 = Leaf(60, 80, "grandchild2")
    child1.add_child(grandchild1)
    child2.add_child(grandchild2)

    print("\n3. Tree visualization")
    # Default visualization
    print("Default:")
    tree.visualize()

    # Custom visualizations
    print("\nWith Position objects:")
    TreeVisualizer.visualize(tree,
                             VisualizationConfig(position_format='position'))

    print("\nWith tuples and children count:")
    TreeVisualizer.visualize(
        tree,
        VisualizationConfig(position_format='tuple',
                            show_children_count=True,
                            show_size=False))

    print("\n4. Accessing properties")
    print(f"Root size: {root.size}")
    print(f"Child1 start: {child1.start}, end: {child1.end}")

    print("\n5. Finding nodes")
    best_match = tree.find_best_match(20, 30)
    print(f"Best match for (20, 30): {best_match}")

    common_ancestor = grandchild1.find_common_ancestor(grandchild2)
    print(f"Common ancestor of grandchildren: {common_ancestor}")

    multi_child = grandchild1.find_first_multi_child_ancestor()
    print(f"First multi-child ancestor: {multi_child}")

    print("\n6. Flattening tree")
    flat_list = tree.flatten()
    print("Flattened tree:", [leaf.info for leaf in flat_list])

    print("\n7. JSON serialization")
    json_str = tree.to_json()
    print("JSON string:", dumps(loads(json_str), indent=2))

    print("\n8. JSON deserialization")
    loaded_tree = Tree.from_json(json_str)
    print("Loaded tree:")
    loaded_tree.visualize()


def example_ast_tree():
    """Example of using AstTreeBuilder"""
    # Get current frame
    frame = currentframe()

    # Build AST tree
    builder = AstTreeBuilder(frame)
    ast_tree = builder.build()

    print("\nAST Tree visualization:")
    ast_tree.visualize()

    # Print flattened nodes
    print("\nFlattened AST nodes:")
    for leaf in ast_tree.flatten():
        print(f"{leaf.info}: [{leaf.start}, {leaf.end}]")


if __name__ == "__main__":
    example_all_methods()
    example_ast_tree()
