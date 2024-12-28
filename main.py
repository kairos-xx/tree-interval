"""
Comprehensive demonstration of all features of the tree interval package.
"""

from inspect import currentframe

from rich.style import Style

from src.tree_interval import FrameAnalyzer
from src.tree_interval import Leaf
from src.tree_interval import Position
from src.tree_interval import Tree
from src.tree_interval import TreeVisualizer
from src.tree_interval import VisualizationConfig
from src.tree_interval.rich_printer import RichPrintConfig
from src.tree_interval.rich_printer import RichTreePrinter


def demonstrate_positions():
    print("\n=== Position Examples ===")
    # Basic Position
    pos1 = Position(0, 100)
    leaf1 = Leaf(pos1, info="Root")
    print("Basic position:", f"start={pos1.start}, end={pos1.end}")

    # Position with line numbers
    pos2 = Position(10, 50)
    pos2.lineno = 1
    pos2.end_lineno = 5
    print("Position with lines:",
          f"lineno={pos2.lineno}, end_lineno={pos2.end_lineno}")

    # Position with column offsets
    pos3 = Position(60, 90)
    pos3.col_offset = 4
    pos3.end_col_offset = 8
    print(
        "Position with columns:",
        f"col_offset={pos3.col_offset}, end_col_offset={pos3.end_col_offset}",
    )

    # Position with absolute positions
    pos4 = Position(30, 70)
    print(
        "Absolute positions:",
        f"absolute_start={pos4.absolute_start}, absolute_end={pos4.absolute_end}",
    )

    # Different position formats
    print("Position format:", pos4.position_as("position"))
    print("Tuple format:", pos4.position_as("tuple"))
    print("Default format:", pos4.position_as())


def demonstrate_find_nodes():
    print("\n=== Find Nodes Example ===")
    # Create a tree structure
    tree = Tree("Find Example")
    root = Leaf(Position(0, 100), info={"type": "Module"})

    child1_pos = Position(10, 40)
    child1_pos.lineno = 2
    child1_pos.end_lineno = 4
    child1_pos.col_offset = 4
    child1_pos.end_col_offset = 40
    child1 = Leaf(child1_pos, info={"type": "FunctionDef", "name": "hello"})

    child2_pos = Position(50, 90)
    child2_pos.lineno = 5
    child2_pos.end_lineno = 8
    child2_pos.col_offset = 4
    child2_pos.end_col_offset = 90
    child2 = Leaf(child2_pos, info={"type": "ClassDef", "name": "MyClass"})

    grandchild_pos = Position(20, 30)
    grandchild_pos.lineno = 3
    grandchild_pos.end_lineno = 3
    grandchild_pos.col_offset = 8
    grandchild_pos.end_col_offset = 30
    grandchild = Leaf(grandchild_pos, info={"type": "Return"})

    # Build the tree
    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild)

    # Find parent example
    found_parent = grandchild.find_parent(lambda n: isinstance(
        n.info, dict) and n.info.get("type") == "FunctionDef")
    print("Found parent:", found_parent.info if found_parent else None)

    # Find child example
    found_child = root.find_child(lambda n: isinstance(n.info, dict) and n.info
                                  .get("type") == "ClassDef")
    print("Found child:", found_child.info if found_child else None)

    # Find sibling example
    found_sibling = child1.find_sibling(lambda n: isinstance(n.info, dict) and
                                        n.info.get("type") == "ClassDef")
    print("Found sibling:", found_sibling.info if found_sibling else None)


def demonstrate_leaves():
    print("\n=== Leaf Examples ===")
    # Create leaf with Position object
    leaf1 = Leaf(Position(0, 100), info="Using Position")
    print("Leaf from Position:", leaf1)

    # Create leaf with tuple
    leaf2 = Leaf(10, 50, "Using Tuple")
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
    root = Leaf(Position(0, 100), info="root")
    root.position.lineno = 1
    root.position.end_lineno = 10
    root.position.col_offset = 0
    root.position.end_col_offset = 80
    tree.root = root

    child1 = Leaf(Position(10, 40), info="child1")
    child1.position.lineno = 2
    child1.position.end_lineno = 4
    child1.position.col_offset = 4

    child2 = Leaf(Position(50, 90), info="child2")
    child2.position.lineno = 5
    child2.position.end_lineno = 8
    child2.position.col_offset = 4

    grandchild1 = Leaf(Position(15, 25), info="grandchild1")
    grandchild1.position.lineno = 3
    grandchild1.position.end_lineno = 3
    grandchild1.position.col_offset = 8

    grandchild2 = Leaf(Position(60, 80), info="grandchild2")
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
    print(
        f"Best match for (20, 30): {best_match.info if best_match else None}")

    common_ancestor = grandchild1.find_common_ancestor(grandchild2)
    print(
        f"Common ancestor of grandchildren: {common_ancestor.info if common_ancestor else None}"
    )

    multi_child = grandchild1.find_first_multi_child_ancestor()
    print(
        f"First multi-child ancestor: {multi_child.info if multi_child else None}"
    )

    # Tree traversal
    print("\nTree Traversal:")
    flat_list = tree.flatten()
    print("Flattened tree:", flat_list)

    # Different visualization methods
    print("\nVisualization Methods:")
    print("\n1. Default visualization:")
    tree.visualize()

    print("\n2. Position format:")
    TreeVisualizer.visualize(tree,
                             VisualizationConfig(position_format="position"))

    print("\n3. Tuple format with children count:")
    TreeVisualizer.visualize(
        tree,
        VisualizationConfig(position_format="tuple",
                            show_children_count=True,
                            show_size=False),
    )

    # JSON operations
    print("\nJSON Operations:")
    json_str = tree.to_json()
    print("Tree as JSON:", json_str)

    print("\nRecreated from JSON:")
    new_tree = Tree.from_json(json_str)
    new_tree.visualize()

    return tree


def demonstrate_frame_analyzer():
    print("\n=== Frame Analyzer Demo ===")

    def analyze_this():
        x = 1 + 2  # This line will be analyzed
        analyzer = FrameAnalyzer(currentframe())

        # Show current node
        current_node = analyzer.find_current_node()
        print("Current Node Information:")
        print(f"Node: {current_node if current_node else None}")
        # Build and show tree
        tree = analyzer.build_tree()

        if tree and tree.root:
            print("\nFull AST Tree:")
            printer = RichTreePrinter()
            printer.print_tree(tree)
            TreeVisualizer.visualize(
                tree, VisualizationConfig(position_format="position"))

        return x

    # Execute the function to perform analysis
    analyze_this()


def demonstrate_line_positions():
    print("\n=== Line Position Examples ===")

    # Create a tree with line numbers
    tree = Tree("Line Number Example")

    # Create root with line numbers
    root = Leaf(Position(0, 100), info="Function")
    root.position.lineno = 1
    root.position.end_lineno = 10
    root.position.col_offset = 0
    root.position.end_col_offset = 4
    tree.root = root

    # Create a child node (if statement)
    if_node = Leaf(Position(20, 60), info="If Block")
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
                             VisualizationConfig(position_format="position"))


def demonstrate_basic_rich_printing():
    """Basic Rich tree printing example."""
    print("\n=== Basic Rich Printing ===")
    tree = Tree("Basic Example")

    root = Leaf(Position(0, 100), info={"type": "Module", "name": "example"})
    child1 = Leaf(Position(10, 40), info={"type": "Function", "name": "hello"})
    child2 = Leaf(Position(50, 90), info={"type": "Class", "name": "MyClass"})

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    printer = RichTreePrinter()
    printer.print_tree(tree)


def demonstrate_custom_config():
    """Rich printing with custom configuration."""
    print("\n=== Custom Rich Printing ===")
    tree = Tree("Custom Style Example")

    root = Leaf(Position(0, 100), {"type": "Program"})
    child = Leaf(Position(10, 50), {"type": "Variable"})
    tree.root = root
    tree.add_leaf(child)

    config = RichPrintConfig(
        show_size=True,
        show_info=True,
        root_style=Style(color="magenta", bold=True),
        node_style=Style(color="yellow"),
        leaf_style=Style(color="green"),
    )

    printer = RichTreePrinter(config)
    printer.print_tree(tree)


def demonstrate_ast_rich_printing():
    """AST visualization with Rich printer."""
    print("\n=== AST Rich Printing ===")
    tree = Tree("AST Example")

    root = Leaf(Position(0, 100), info={"type": "Module"})
    func_def = Leaf(Position(10, 90),
                    info={
                        "type": "FunctionDef",
                        "name": "example"
                    })
    args = Leaf(Position(20, 30), info={"type": "Arguments"})
    body = Leaf(Position(40, 80), info={"type": "Body"})

    tree.root = root
    tree.add_leaf(func_def)
    func_def.add_child(args)
    func_def.add_child(body)

    printer = RichTreePrinter(RichPrintConfig(show_position=True))
    printer.print_tree(tree)


def demonstrate_nested_attributes():
    """Example showing nested attribute access"""
    tree = Tree("Nested Attributes Example")
    root = Leaf(Position(0, 100), info="Root Node")
    child = Leaf(Position(10, 50), info="Child Node")

    root.position.lineno = 1
    root.position.end_lineno = 5
    root.position.col_offset = 0
    root.position.end_col_offset = 20

    tree.root = root
    tree.add_leaf(child)

    # Initialize nested attributes
    root._as_dict()

    # Access nested attributes
    print("=== Nested Attributes Example ===")
    print(f"Start position: {root.attributes.start}")
    print(f"Size: {root.attributes.size}")
    print(f"Line number: {root.attributes.position.lineno}")
    print(f"Column offset: {root.attributes.position.col_offset}")


def demonstrate_find_method():
    """Example showing the find method and dot notation"""
    print("\n=== Find Method Example ===")

    # Create a tree structure
    root = Leaf(Position(0, 100), info={"type": "Module", "name": "main"})
    child1 = Leaf(Position(10, 40),
                  info={
                      "type": "FunctionDef",
                      "name": "hello"
                  })
    child2 = Leaf(Position(50, 90),
                  info={
                      "type": "ClassDef",
                      "name": "MyClass"
                  })
    grandchild = Leaf(Position(20, 30), info={"type": "Return"})

    # Build tree
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    # Build tree structure first
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    # Initialize attributes after tree structure is complete
    root._as_dict()
    child1._as_dict()
    child2._as_dict()
    grandchild._as_dict()

    # Use find method with dot notation
    found = root.find(
        lambda n: isinstance(n.info, dict) and n.info.get("name") == "hello")
    print(f"Found function: {found.info if found else None}")

    found = child1.find(lambda n: isinstance(n.info, dict) and n.info.get(
        "type") == "ClassDef")
    print(f"Found class: {found.info if found else None}")

    found = grandchild.find(
        lambda n: isinstance(n.info, dict) and n.info.get("type") == "Module")
    print(f"Found module: {found.info if found else None}")


def demonstrate_leaf_navigation():
    print("\n=== Leaf Navigation Example ===")
    # Create a tree and nodes
    tree = Tree("Navigation Example")

    # Create test nodes
    grand_parent = Leaf(Position(0, 400), info="Grand Parent")
    parent1 = Leaf(Position(0, 200), info="Parent 1")
    parent2 = Leaf(Position(200, 400), info="Parent 2")
    parent1_child1 = Leaf(Position(0, 100), info="Child 1.1")
    parent1_child2 = Leaf(Position(100, 200), info="Child 1.2")
    parent2_child1 = Leaf(Position(200, 300), info="Child 2.1")
    parent2_child2 = Leaf(Position(300, 400), info="Child 2.2")

    # Build tree structure
    tree.root = grand_parent
    grand_parent.add_child(parent1)
    grand_parent.add_child(parent2)
    parent1.add_child(parent1_child1)
    parent1.add_child(parent1_child2)
    parent2.add_child(parent2_child1)
    parent2.add_child(parent2_child2)

    # Test parent relationship
    parent_node = parent1_child1.parent
    parent_info = parent_node.info if parent_node else None
    print(f"Child 1.1's parent: {parent_info}")

    # Test next relationship
    next_node = parent1_child1.next
    next_info = next_node.info if next_node else None
    print(f"Child 1.1's next sibling: {next_info}")

    # Test previous relationship
    prev_node = parent1_child2.previous
    prev_info = prev_node.info if prev_node else None
    print(f"Child 1.2's previous sibling: {prev_info}")

    # Test parent navigation
    print(
        f"Parent 1's next sibling: {parent1.next.info if parent1.next else None}"
    )


def demonstrate_node_navigation():
    print("\n=== Node Navigation Examples ===")

    # Create a program structure tree
    program = Leaf(Position(0, 500), info="Program")
    class_def = Leaf(Position(0, 250), info="Class: MyClass")
    function_def = Leaf(Position(250, 500), info="Function: process_data")

    method1 = Leaf(Position(50, 120), info="Method: __init__")
    method2 = Leaf(Position(130, 200), info="Method: validate")

    param1 = Leaf(Position(270, 300), info="Parameter: data")
    param2 = Leaf(Position(310, 340), info="Parameter: options")

    # Build tree relationships
    program.add_child(class_def)
    program.add_child(function_def)
    class_def.add_child(method1)
    class_def.add_child(method2)
    function_def.add_child(param1)
    function_def.add_child(param2)

    # Demonstrate navigation
    print(f"First method's parent: {method1.parent.info}"
          )  # Shows class definition
    print(f"First method's next sibling: {method1.next.info}"
          )  # Shows the validate method
    print(f"Second method's previous sibling: {method2.previous.info}"
          )  # Shows the init method
    print(f"Function's first parameter: {function_def.children[0].info}"
          )  # Shows first parameter


def main():
    print("=== Tree Interval Package Demo ===")
    demonstrate_positions()
    demonstrate_find_nodes()
    demonstrate_leaves()
    demonstrate_tree_operations()
    demonstrate_frame_analyzer()
    demonstrate_line_positions()
    demonstrate_basic_rich_printing()
    demonstrate_custom_config()
    demonstrate_ast_rich_printing()
    demonstrate_nested_attributes()
    demonstrate_find_method()
    demonstrate_leaf_navigation()
    demonstrate_node_navigation()


if __name__ == "__main__":
    main()
