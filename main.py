
import sys
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

def demonstrate_positions():
    print_header("Position Examples", GREEN)
    pos = Position(0, 100)
    pos.lineno = 1
    pos.end_lineno = 5
    pos.col_offset = 0
    pos.end_col_offset = 20
    print(f"{GREEN}Position: {pos.position_as('position')}{RESET}")

def demonstrate_leaves():
    print_header("Leaf Examples", YELLOW)
    leaf1 = Leaf(Position(0, 100, "Using Position"))
    print(f"{YELLOW}Leaf from Position: {leaf1}{RESET}")
    leaf2 = Leaf((10, 50, "Using Tuple"))
    print(f"{YELLOW}Leaf from tuple: {leaf2}{RESET}")

def demonstrate_tree_operations():
    print_header("Tree Operations", BLUE)
    tree = Tree("Example")
    root = Leaf(Position(0, 100), info="Root Node")
    child = Leaf(Position(10, 50), info="Child Node")
    tree.root = root
    tree.add_leaf(child)
    print(f"{BLUE}Tree structure:{RESET}")
    tree.visualize()

def demonstrate_frame_analysis():
    print_header("Frame Analysis", MAGENTA)
    analyzer = FrameAnalyzer(sys._getframe())
    tree = analyzer.build_tree()
    if tree and tree.root:
        print(f"{MAGENTA}Current frame analyzed successfully{RESET}")
        tree.visualize()

def demonstrate_tree_search():
    print_header("Tree Search Operations", CYAN)
    tree = Tree("Search Example")
    root = Leaf(Position(0, 100), info="Root")
    child = Leaf(Position(10, 50), info="Child")
    tree.root = root
    tree.add_leaf(child)
    result = tree.find_best_match(10, 50)
    if result:
        print(f"{CYAN}Found node at position: {result.position_as()}{RESET}")

def main():
    print_header("Tree Interval Package Demo", BLUE)
    demonstrate_positions()
    demonstrate_leaves()
    demonstrate_tree_operations()
    demonstrate_frame_analysis()
    demonstrate_tree_search()

if __name__ == "__main__":
    main()
