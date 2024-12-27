"""
Tree Interval Package Demo
"""
from src.tree_interval import Leaf, Tree, TreeVisualizer, VisualizationConfig


def main():
    # Create a basic tree
    tree = Tree("Example")
    root = Leaf(0, 100, "Root")
    child1 = Leaf(10, 40, "Child 1")
    child2 = Leaf(50, 90, "Child 2")
    grandchild = Leaf(15, 35, "Grandchild")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild)

    print("\nBasic Tree:")
    tree.visualize()

    # Demonstrate different visualization options
    print("\nWith position objects:")
    TreeVisualizer.visualize(tree,
                             VisualizationConfig(position_format="position"))

    print("\nWith tuples and children count:")
    TreeVisualizer.visualize(
        tree,
        VisualizationConfig(position_format="tuple",
                            show_children_count=True,
                            show_size=False),
    )

    # Demonstrate JSON serialization
    json_str = tree.to_json()
    print("\nJSON representation:", json_str)

    loaded_tree = Tree.from_json(json_str)
    print("\nDeserialized tree:")
    loaded_tree.visualize()


if __name__ == "__main__":
    main()
