"""
Comprehensive demonstration of all features of the tree interval package.
"""

from inspect import currentframe

from src.tree_interval import (
    FrameAnalyzer,
    Leaf,
    Position,
    Tree,
    TreeVisualizer,
    VisualizationConfig,
)


def demonstrate_positions():
    print("\n=== Position Examples ===")
    # Basic Position
    pos1 = Position(0, 100, "Root")
    print("Basic position:", f"start={pos1.start}, end={pos1.end}, info={pos1.info}")

    # Position with line numbers
    pos2 = Position(10, 50, "With Lines")
    pos2.lineno = 1
    pos2.end_lineno = 5
    print("Position with lines:", f"lineno={pos2.lineno}, end_lineno={pos2.end_lineno}")

    # Position with column offsets
    pos3 = Position(60, 90, "With Columns")
    pos3.col_offset = 4
    pos3.end_col_offset = 8
    print(
        "Position with columns:",
        f"col_offset={pos3.col_offset}, end_col_offset={pos3.end_col_offset}",
    )

    # Position with absolute positions
    pos4 = Position(30, 70, "Absolute")
    print(
        "Absolute positions:",
        f"absolute_start={pos4.absolute_start}, absolute_end={pos4.absolute_end}",
    )


def demonstrate_leaves():
    print("\n=== Leaf Examples ===")
    # Create leaf with Position object
    leaf1 = Leaf(Position(0, 100, "Using Position"))
    print("Leaf from Position:", leaf1)

    # Create leaf with tuple
    leaf2 = Leaf((10, 50, "Using Tuple"))
    print("Leaf from tuple:", leaf2)

    # Create leaf with separate arguments
    leaf3 = Leaf(60, 90, "Using Args")
    print("Leaf from args:", leaf3)


def demonstrate_tree_operations():
    print("\n=== Tree Operations ===")
    # Create tree
    tree = Tree[str]("Example Code", start_lineno=1, indent_size=4)
    print("Tree created with source:", tree.source)

    # Build hierarchy with line numbers
    root = Leaf(Position(0, 100, "root"))
    root.position.lineno = 1
    root.position.end_lineno = 10
    tree.root = root

    child1 = Leaf(Position(10, 40, "child1"))
    child1.position.lineno = 2
    child1.position.end_lineno = 4
    child1.position.col_offset = 4

    child2 = Leaf(Position(50, 90, "child2"))
    child2.position.lineno = 5
    child2.position.end_lineno = 8
    child2.position.col_offset = 4

    grandchild1 = Leaf(Position(15, 25, "grandchild1"))
    grandchild1.position.lineno = 3
    grandchild1.position.end_lineno = 3
    grandchild1.position.col_offset = 8

    grandchild2 = Leaf(Position(60, 80, "grandchild2"))
    grandchild2.position.lineno = 6
    grandchild2.position.end_lineno = 7
    grandchild2.position.col_offset = 8

    # Add nodes
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild1)
    child2.add_child(grandchild2)

    return tree


def example_basic_tree():
    """Basic tree creation and visualization."""
    tree = Tree("Basic Example")
    root = Leaf(0, 100, "Root")
    child1 = Leaf(10, 40, "Child 1")
    child2 = Leaf(50, 90, "Child 2")
    grandchild = Leaf(15, 35, "Grandchild")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild)

    print("Basic Tree:")
    tree.visualize()


def example_custom_visualization():
    """Demonstrate different visualization options."""
    tree = Tree("Visualization Example")
    root = Leaf(0, 100, "Root")
    child1 = Leaf(10, 40, "Child 1")
    child2 = Leaf(50, 90, "Child 2")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    print("\nDefault visualization:")
    tree.visualize()

    print("\nWith position objects:")
    TreeVisualizer.visualize(tree, VisualizationConfig(position_format="position"))

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
    root = Leaf(0, 100, "Root")
    child = Leaf(10, 50, "Child")
    tree.root = root
    tree.add_leaf(child)

    # Serialize to JSON
    json_str = tree.to_json()
    print("JSON representation:", json_str)

    # Deserialize from JSON
    loaded_tree = Tree.from_json(json_str)
    print("\nDeserialized tree:")
    loaded_tree.visualize()


def demonstrate_line_positions():
    print("\n=== Line Position Examples ===")

    # Create a tree with line numbers
    tree = Tree("Line Number Example")

    # Create root with line numbers
    root = Leaf(Position(0, 100, "Function"))
    root.position.lineno = 1
    root.position.end_lineno = 10
    root.position.col_offset = 0
    root.position.end_col_offset = 4
    tree.root = root

    # Create a child node (if statement)
    if_node = Leaf(Position(20, 60, "If Block"))
    if_node.position.lineno = 3
    if_node.position.end_lineno = 5
    if_node.position.col_offset = 4
    if_node.position.end_col_offset = 8
    tree.add_leaf(if_node)

    # Visualize with different configs
    print("\nDefault view:")
    tree.visualize()

    print("\nDetailed position view:")
    TreeVisualizer.visualize(tree, VisualizationConfig(position_format="position"))


if __name__ == "__main__":
    print("=== Tree Interval Package Demo ===")
    demonstrate_positions()
    demonstrate_leaves()
    demonstrate_tree_operations()
    example_basic_tree()
    example_custom_visualization()
    example_json_serialization()
    demonstrate_line_positions()
