
"""
Comprehensive examples demonstrating all features of the tree interval package.
"""
from src.tree_interval import Tree, Leaf, Position, TreeVisualizer, VisualizationConfig

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

def demonstrate_leaves():
    # Create leaf with Position object
    leaf1 = Leaf(Position(0, 100, "Using Position"))
    
    # Create leaf with tuple
    leaf2 = Leaf((10, 50, "Using Tuple"))
    
    # Create leaf with separate arguments
    leaf3 = Leaf(60, 90, "Using Args")
    
    return [leaf1, leaf2, leaf3]

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
    leaves = demonstrate_leaves()
    for leaf in leaves:
        print(f"Leaf: {leaf.start}-{leaf.end} ({leaf.info})")
    
    print("\n=== Tree Operations ===")
    tree = demonstrate_tree_operations()
    
    print("\nDefault visualization:")
    tree.visualize()
    
    print("\nWith Position format:")
    TreeVisualizer.visualize(tree, 
        VisualizationConfig(position_format='position'))
    
    print("\nWith tuples and children count:")
    TreeVisualizer.visualize(tree, 
        VisualizationConfig(position_format='tuple',
                           show_children_count=True,
                           show_size=False))
    
    print("\nFinding nodes:")
    best_match = tree.find_best_match(20, 30)
    print(f"Best match for (20, 30): {best_match}")
    
    print("\nTree traversal:")
    flat_list = tree.flatten()
    print("Flattened tree:", [leaf.info for leaf in flat_list])
    
    print("\nJSON operations:")
    json_str = tree.to_json()
    print("JSON:", json_str)
    
    new_tree = Tree.from_json(json_str)
    print("\nReconstructed tree:")
    new_tree.visualize()

if __name__ == "__main__":
    main()
