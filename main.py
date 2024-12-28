
"""
Comprehensive demonstration of all features of the tree interval package.
"""

import sys
from inspect import currentframe
from src.tree_interval import (
    FrameAnalyzer,
    Leaf,
    Position,
    Tree,
    TreeVisualizer,
    VisualizationConfig,
)

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

def print_header(title, color=BLUE):
    """Print a section header with ASCII borders."""
    width = 60
    print(f"\n{color}╔{'═' * (width-2)}╗")
    print(f"║{title.center(width-2)}║")
    print(f"╚{'═' * (width-2)}╝{RESET}\n")

def print_tree(node, prefix="", is_last=True):
    """Print tree structure using ASCII characters."""
    if node is None:
        return
    
    branch = "└── " if is_last else "├── "
    print(prefix + branch + str(node.info))
    
    prefix += "    " if is_last else "│   "
    for i, child in enumerate(node.children):
        print_tree(child, prefix, i == len(node.children) - 1)

def demonstrate_positions():
    print_header("Position Examples", GREEN)
    pos1 = Position(0, 100)
    print("Basic position:", f"start={pos1.start}, end={pos1.end}")

    pos2 = Position(10, 50)
    pos2.lineno = 1
    pos2.end_lineno = 5
    print("Position with lines:", f"lineno={pos2.lineno}, end_lineno={pos2.end_lineno}")

    pos3 = Position(60, 90)
    pos3.col_offset = 4
    pos3.end_col_offset = 8
    print("Position with columns:", f"col_offset={pos3.col_offset}, end_col_offset={pos3.end_col_offset}")

    pos4 = Position(30, 70)
    print("Absolute positions:", f"absolute_start={pos4.absolute_start}, absolute_end={pos4.absolute_end}")

    print("Position format:", pos4.position_as("position"))
    print("Tuple format:", pos4.position_as("tuple"))
    print("Default format:", pos4.position_as())

def demonstrate_leaves():
    print_header("Leaf Examples", YELLOW)
    leaf1 = Leaf(Position(0, 100), info="Using Position")
    print("Leaf from Position:", leaf1)

    leaf2 = Leaf((10, 50, "Using Tuple"))
    print("Leaf from tuple:", leaf2)

    leaf3 = Leaf(60, 90, "Using Args")
    print("Leaf from args:", leaf3)

def demonstrate_tree_operations():
    print_header("Tree Operations", BLUE)
    tree = Tree("Example Tree")
    root = Leaf(Position(0, 100), info="Root")
    child1 = Leaf(Position(10, 40), info="Child 1")
    child2 = Leaf(Position(50, 90), info="Child 2")
    
    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    
    print("\nTree Structure:")
    print_tree(tree.root)

def demonstrate_frame_analyzer():
    print_header("Frame Analyzer Demo", MAGENTA)
    analyzer = FrameAnalyzer(currentframe())
    tree = analyzer.build_tree()
    if tree and tree.root:
        print("Frame Analysis Tree:")
        print_tree(tree.root)

def demonstrate_node_navigation():
    print_header("Node Navigation Examples", CYAN)
    root = Leaf(Position(0, 100), info="Root")
    child1 = Leaf(Position(10, 40), info="Child 1")
    child2 = Leaf(Position(50, 90), info="Child 2")
    grandchild = Leaf(Position(15, 35), info="Grandchild")
    
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)
    
    print("Navigation Tree:")
    print_tree(root)
    
    print("\nNavigation Info:")
    print(f"Child 1's parent: {child1.parent.info if child1.parent else None}")
    print(f"Child 1's next sibling: {child1.next.info if child1.next else None}")
    print(f"Child 2's previous sibling: {child2.previous.info if child2.previous else None}")

def main():
    print_header("Tree Interval Package Demo", BLUE)
    demonstrate_positions()
    demonstrate_leaves()
    demonstrate_tree_operations()
    demonstrate_frame_analyzer()
    demonstrate_node_navigation()

if __name__ == "__main__":
    main()
