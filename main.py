
"""
Comprehensive example demonstrating all features of the tree structure.
"""

from src.tree_interval import Tree, Leaf, Position, TreeVisualizer, VisualizationConfig

def demonstrate_all_features():
    # 1. Create a tree
    print("\n1. Tree Creation")
    tree = Tree[str]("Example code", start_lineno=1, indent_size=4)
    root = Leaf(Position(0, 100, "root"))
    tree.root = root

    # 2. Add children
    print("\n2. Adding Children")
    child1 = Leaf(Position(10, 40, "child1"))
    child2 = Leaf(Position(50, 90, "child2"))
    grandchild1 = Leaf(Position(15, 25, "grandchild1"))
    grandchild2 = Leaf(Position(60, 80, "grandchild2"))

    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild1)
    child2.add_child(grandchild2)

    # 3. Tree Visualization Methods
    print("\n3. Different Visualization Methods:")
    print("\nDefault visualization:")
    tree.visualize()

    print("\nWith Position format:")
    TreeVisualizer.visualize(tree, VisualizationConfig(position_format='position'))

    print("\nWith tuples and children count:")
    TreeVisualizer.visualize(tree, VisualizationConfig(
        position_format='tuple',
        show_children_count=True,
        show_size=False
    ))

    # 4. Tree Operations
    print("\n4. Tree Operations:")
    print(f"Root size: {root.size}")
    print(f"Child1 position: ({child1.start}, {child1.end})")
    print(f"Number of root's children: {len(root.children)}")

    # 5. Finding Nodes
    print("\n5. Node Finding:")
    best_match = tree.find_best_match(20, 30)
    print(f"Best match for (20, 30): {best_match}")

    common_ancestor = grandchild1.find_common_ancestor(grandchild2)
    print(f"Common ancestor of grandchildren: {common_ancestor}")

    multi_child = grandchild1.find_first_multi_child_ancestor()
    print(f"First multi-child ancestor: {multi_child}")

    # 6. Tree Traversal
    print("\n6. Tree Traversal:")
    flat_list = tree.flatten()
    print("Flattened tree:", [leaf.info for leaf in flat_list])

    # 7. JSON Serialization
    print("\n7. JSON Operations:")
    json_str = tree.to_json()
    print("JSON string:", json_str)
    
    # Recreate tree from JSON
    new_tree = Tree.from_json(json_str)
    print("\nReconstructed tree visualization:")
    new_tree.visualize()

if __name__ == "__main__":
    demonstrate_all_features()
