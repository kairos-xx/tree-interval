"""
Comprehensive examples demonstrating all features of the tree interval package.
"""

from src.tree_interval import Leaf, Position, Tree, VisualizationConfig


def demonstrate_positions():
    # Basic Position
    pos1 = Position(0, 100, "Root")

    # Position with line numbers
    pos2 = Position(10, 50, "With Lines")
    pos2.lineno = 1
    pos2.end_lineno = 5

    # Position with column offsets
    pos3 = Position(60, 90, "With Columns")
    pos3.col_offset = 4
    pos3.end_col_offset = 8

    return [pos1, pos2, pos3]


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
    tree.visualize(VisualizationConfig(position_format="position"))

    print("\nWith tuples and children count:")
    tree.visualize(
        VisualizationConfig(position_format="tuple",
                            show_children_count=True,
                            show_size=False))


def demonstrate_tree_operations():
    # Create tree
    tree = Tree[str]("Example", start_lineno=1, indent_size=4)

    # Create hierarchy
    root = Leaf(Position(0, 100, "Root"))
    tree.root = root

    # Add children
    child1 = Leaf(Position(10, 40, "Child 1"))
    child2 = Leaf(Position(50, 90, "Child 2"))
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    # Add grandchildren
    grandchild1 = Leaf(Position(15, 25, "Grandchild 1"))
    grandchild2 = Leaf(Position(60, 80, "Grandchild 2"))
    child1.add_child(grandchild1)
    child2.add_child(grandchild2)

    return tree


def main():
    print("=== Position Examples ===")
    positions = demonstrate_positions()
    for pos in positions:
        print(f"Position: {pos.start}-{pos.end} ({pos.info})")

    print("\n=== Leaf Examples ===")
    tree = demonstrate_tree_operations()
    leaves = tree.flatten()
    for leaf in leaves:
        print(f"Leaf: {leaf.start}-{leaf.end} ({leaf.info})")

    print("\n=== Tree Operations ===")
    tree = demonstrate_tree_operations()
    tree_json = tree.to_json()

    print("\nDefault visualization:")
    tree.visualize()

    print("\nWith Position format:")
    tree.visualize(VisualizationConfig(position_format="position"))

    print("\nWith tuples and children count:")
    tree.visualize(
        VisualizationConfig(position_format="tuple",
                            show_children_count=True,
                            show_size=False))

    print("\nFinding nodes:")
    best_match = tree.find_best_match(20, 30)
    print(f"Best match for (20, 30): {best_match}")

    print("\nTree traversal:")
    flat_list = tree.flatten()
    print("Flattened tree:", [leaf.info for leaf in flat_list])

    print("\nJSON operations:")
    print("JSON:", tree_json)

    new_tree = Tree.from_json(tree_json)
    print("\nReconstructed tree:")
    new_tree.visualize()


if __name__ == "__main__":
    print("=== Basic Tree Example ===")
    example_basic_tree()
    print("\n=== Visualization Options Example ===")
    example_custom_visualization()
    main()
