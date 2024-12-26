
"""
Comprehensive demonstration of all features of the tree interval package.
"""
from inspect import currentframe
from src.tree_interval import Tree, Leaf, Position, TreeVisualizer, VisualizationConfig


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
    print("Position with columns:", f"col_offset={pos3.col_offset}, end_col_offset={pos3.end_col_offset}")
    
    # Position with absolute positions
    pos4 = Position(30, 70, "Absolute")
    print("Absolute positions:", f"absolute_start={pos4.absolute_start}, absolute_end={pos4.absolute_end}")

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
    
    # Tree information
    print("\nTree Information:")
    print(f"Root size: {root.size}")
    print(f"Number of root's children: {len(root.children)}")
    print(f"Child1 position: ({child1.start}, {child1.end})")
    
    # Node finding
    print("\nNode Finding:")
    best_match = tree.find_best_match(20, 30)
    print(f"Best match for (20, 30): {best_match}")
    
    common_ancestor = grandchild1.find_common_ancestor(grandchild2)
    print(f"Common ancestor of grandchildren: {common_ancestor}")
    
    multi_child = grandchild1.find_first_multi_child_ancestor()
    print(f"First multi-child ancestor: {multi_child}")
    
    # Tree traversal
    print("\nTree Traversal:")
    flat_list = tree.flatten()
    print("Flattened tree:", [leaf.info for leaf in flat_list])
    
    # Different visualization methods
    print("\nVisualization Methods:")
    print("\n1. Default visualization:")
    tree.visualize()
    
    print("\n2. Position format:")
    TreeVisualizer.visualize(tree, VisualizationConfig(position_format='position'))
    
    print("\n3. Tuple format with children count:")
    TreeVisualizer.visualize(tree, VisualizationConfig(
        position_format='tuple',
        show_children_count=True,
        show_size=False
    ))
    
    # JSON operations
    print("\nJSON Operations:")
    json_str = tree.to_json()
    print("Tree as JSON:", json_str)
    
    print("\nRecreated from JSON:")
    new_tree = Tree.from_json(json_str)
    new_tree.visualize()
    
    return tree

import sys
from src.tree_interval import FrameAnalyzer

def demonstrate_frame_analyzer():
    print("\n=== Frame Analyzer Demo ===")
    
    def sample_code():
        a = 1
        b = 2
        c = a + b
        return c
    
    # Get the frame by executing the function
    frame = sys._getframe()
    analyzer = FrameAnalyzer(frame)
    
    # Show current node
    current_node = analyzer.find_current_node()
    print("Current Node Information:")
    print(f"Node: {current_node}")
    
    # Build and show tree
    tree = analyzer.build_tree()
    if tree:
        print("\nFull AST Tree:")
        TreeVisualizer.visualize(tree, VisualizationConfig(
            position_format='position',
            show_children_count=True
        ))
    
    
   

if __name__ == "__main__":
    print("=== Tree Interval Package Demo ===")
    demonstrate_positions()
    demonstrate_leaves()
    demonstrate_tree_operations()
    demonstrate_frame_analyzer()
