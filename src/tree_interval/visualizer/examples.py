"""Examples demonstrating tree visualizer functionality."""

from src.tree_interval import Leaf, Tree, TreeVisualizer, VisualizationConfig


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


if __name__ == "__main__":
    print("=== Basic Tree Example ===")
    example_basic_tree()

    print("\n=== Visualization Options Example ===")
    example_custom_visualization()

    print("\n=== JSON Serialization Example ===")
    example_json_serialization()
