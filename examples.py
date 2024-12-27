"""
Comprehensive examples demonstrating all features of the tree interval package.
"""
from src.tree_interval import Tree, Leaf, Position, FrameAnalyzer, VisualizationConfig
from inspect import currentframe

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
    TreeVisualizer.visualize(tree, 
        VisualizationConfig(position_format='position'))

if __name__ == "__main__":
    main()
    demonstrate_line_positions()

    
    new_tree = Tree.from_json(json_str)
    print("\nReconstructed tree:")
    new_tree.visualize()

if __name__ == "__main__":
    main()
def example_frame_analyzer():
    """Demonstrate frame analyzer functionality."""
    def sample_function():
        x = 1
        y = 2
        return x + y

    # Get current frame
    frame = currentframe()
    
    # Create analyzer
    analyzer = FrameAnalyzer(frame)
    
    # Find current node
    current_node = analyzer.find_current_node()
    print("\nCurrent Node:", current_node)
    
    # Build and show complete tree
    tree = analyzer.build_tree()
    if tree:
        print("\nComplete AST Tree:")
        tree.visualize()

if __name__ == "__main__":
    print("=== Basic Tree Example ===")
    example_basic_tree()
    print("\n=== Visualization Options Example ===")
    example_custom_visualization()
    print("\n=== Frame Analyzer Example ===")
    example_frame_analyzer()