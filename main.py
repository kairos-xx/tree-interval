
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

def main():
    # Basic Tree Demo
    print_header("Basic Tree Operations", BLUE)
    tree = Tree("Example")
    root = Leaf(Position(0, 100), info="Root Node")
    child = Leaf(Position(10, 50), info="Child Node")
    tree.root = root
    tree.add_leaf(child)
    tree.visualize()

    # Position Demo
    print_header("Position Examples", GREEN)
    pos = Position(0, 100)
    pos.lineno = 1
    pos.end_lineno = 5
    pos.col_offset = 0
    pos.end_col_offset = 20
    print(f"{GREEN}Position: {pos.position_as('position')}{RESET}")

    # Node Navigation
    print_header("Node Navigation", YELLOW)
    child.parent = root
    print(f"{YELLOW}Parent of child: {child.parent.info}{RESET}")
    print(f"{YELLOW}Children of root: {len(root.children)}{RESET}")

    # Frame Analysis
    print_header("Frame Analysis", MAGENTA)
    analyzer = FrameAnalyzer(sys._getframe())
    tree = analyzer.build_tree()
    if tree and tree.root:
        print(f"{MAGENTA}Current frame analyzed successfully{RESET}")
        tree.visualize()

    # Tree Search
    print_header("Tree Search Operations", CYAN)
    result = tree.find_best_match(10, 50)
    if result:
        print(f"{CYAN}Found node at position: {result.position_as()}{RESET}")

if __name__ == "__main__":
    main()
