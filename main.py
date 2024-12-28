
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

def demonstrate_positions():
    """Demonstrates basic Position class usage."""
    print_header("Position Examples", GREEN)
    pos1 = Position(0, 100)
    print(f"{GREEN}Basic position: start={pos1.start}, end={pos1.end}{RESET}")

    pos2 = Position(10, 50)
    pos2.lineno = 1
    pos2.end_lineno = 5
    print(f"{GREEN}Position with lines: lineno={pos2.lineno}, end_lineno={pos2.end_lineno}{RESET}")

    pos3 = Position(60, 90)
    pos3.col_offset = 4
    pos3.end_col_offset = 8
    print(f"{GREEN}Position with columns: col_offset={pos3.col_offset}, end_col_offset={pos3.end_col_offset}{RESET}")

    pos4 = Position(30, 70)
    print(f"{GREEN}Position formats:")
    print(f"Position: {pos4.position_as('position')}")
    print(f"Tuple: {pos4.position_as('tuple')}")
    print(f"Default: {pos4.position_as()}{RESET}")

def demonstrate_find_nodes():
    """Demonstrates node finding capabilities."""
    print_header("Find Nodes Example", YELLOW)
    tree = Tree("Find Example")
    root = Leaf(Position(0, 100), info={"type": "Module"})
    child1 = Leaf(Position(10, 40), info={"type": "FunctionDef", "name": "hello"})
    child2 = Leaf(Position(50, 90), info={"type": "ClassDef", "name": "MyClass"})
    
    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    
    print(f"{YELLOW}Tree structure:{RESET}")
    tree.visualize()

def demonstrate_tree_operations():
    """Demonstrates tree operations."""
    print_header("Tree Operations", BLUE)
    tree = Tree("Example")
    root = Leaf(Position(0, 100), info="Root Node")
    child = Leaf(Position(10, 50), info="Child Node")
    tree.root = root
    tree.add_leaf(child)
    
    print(f"{BLUE}Tree visualization:{RESET}")
    tree.visualize()

def demonstrate_frame_analysis():
    """Demonstrates frame analysis capabilities."""
    print_header("Frame Analysis", MAGENTA)
    analyzer = FrameAnalyzer(sys._getframe())
    tree = analyzer.build_tree()
    if tree and tree.root:
        print(f"{MAGENTA}Frame analysis tree:{RESET}")
        tree.visualize()

def demonstrate_tree_search():
    """Demonstrates tree search operations."""
    print_header("Tree Search", CYAN)
    tree = Tree("Search Example")
    root = Leaf(Position(0, 100), info="Root")
    child = Leaf(Position(10, 50), info="Target Node")
    tree.root = root
    tree.add_leaf(child)
    
    result = tree.find_best_match(10, 50)
    print(f"{CYAN}Found node: {result.info if result else 'None'}{RESET}")

def main():
    print_header("Tree Interval Package Demo", BLUE)
    demonstrate_positions()
    demonstrate_find_nodes()
    demonstrate_tree_operations()
    demonstrate_frame_analysis()
    demonstrate_tree_search()

if __name__ == "__main__":
    main()
