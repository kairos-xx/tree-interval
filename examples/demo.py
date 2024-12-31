"""
Comprehensive demonstration of all features of the tree interval package.
"""
from rich.style import Style as RichStyle

from src.tree_interval import (
    AstTreeBuilder,
    Leaf,
    Position,
    Tree,
    TreeVisualizer,
    VisualizationConfig,
)
from src.tree_interval.rich_printer import RichTreePrinter
from tree_interval.core.interval_core import PartStatement, Statement


# All demonstrate functions in order of execution
def demonstrate_positions():
    print("\n=== Position Examples ===")
    # Basic Position
    pos1 = Position(0, 100)
    print("Basic position:", f"start={pos1.start}, end={pos1.end}")

    # Position with line numbers
    pos2 = Position(10, 50)
    pos2.lineno = 1
    pos2.end_lineno = 5
    print(
        "Position with lines:",
        f"lineno={pos2.lineno}, end_lineno={pos2.end_lineno}",
    )

    # Position with column offsets
    pos3 = Position(60, 9)
    pos3.col_offset = 4
    pos3.end_col_offset = 8
    print(
        "Position with columns:",
        f"col_offset={pos3.col_offset}, "
        f"end_col_offset={pos3.end_col_offset}",
    )

    # Position with absolute positions
    pos4 = Position(30, 70)
    print(
        "Absolute positions:",
        f"absolute_start={pos4.absolute_start}, "
        f"absolute_end={pos4.absolute_end}",
    )

    # Different position formats
    print("Position format:", pos4.position_as("position"))
    print("Tuple format:", pos4.position_as("tuple"))
    print("Default format:", pos4.position_as())


def demonstrate_leaves():
    print("\n=== Leaf Examples ===")
    # Create leaf with Position object
    leaf1 = Leaf(Position(0, 100), "Using Position")
    print("Leaf from Position:", leaf1)

    # Create leaf with tuple
    leaf2 = Leaf((10, 50), "Using Tuple")
    print("Leaf from tuple:", leaf2)

    # Create leaf with separate arguments
    leaf3 = Leaf(60, "Using Args", 90)
    print("Leaf from args:", leaf3)


def demonstrate_tree_operations():
    """Demonstrates various tree operations including styling."""
    print("\n=== Tree Operations ===")

    # Add styling examples
    print("\n=== Styling Examples ===")
    root = Leaf(Position(0, 100), info={"type": "Module"})
    root.rich_style = RichStyle(color="green", bold=True)

    child = Leaf(Position(10, 50), info={"type": "FunctionDef"})
    child.rich_style = RichStyle(color="blue", bold=False)

    tree = Tree("Styled Example")
    tree.root = root
    tree.add_leaf(child)

    printer = RichTreePrinter()
    printer.print_tree(tree)
    # Create tree
    tree = Tree[str]("Example Code", start_lineno=1, indent_size=4)
    print("Tree created with source:", tree.source)

    # Build hierarchy with line numbers
    root = Leaf(Position(0, 100), "root")
    root.position.lineno = 1
    root.position.end_lineno = 10
    tree.root = root

    child1 = Leaf(Position(10, 40), "child1")
    child1.position.lineno = 2
    child1.position.end_lineno = 4
    child1.position.col_offset = 4

    child2 = Leaf(Position(50, 90), "child2")
    child2.position.lineno = 5
    child2.position.end_lineno = 8
    child2.position.col_offset = 4

    grandchild1 = Leaf(Position(15, 25), "grandchild1")
    grandchild1.position.lineno = 3
    grandchild1.position.end_lineno = 3
    grandchild1.position.col_offset = 8

    grandchild2 = Leaf(Position(60, 80), "grandchild2")
    grandchild2.position.lineno = 6
    grandchild2.position.end_lineno = 7
    grandchild2.position.col_offset = 8

    # Add nodes
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild1)
    child2.add_child(grandchild2)

    return tree


def example_basic_tree():
    """Basic tree creation and visualization."""
    tree = Tree("Basic Example")
    root = Leaf(Position(0, 100), info="Root")
    child1 = Leaf(Position(10, 40), info="Child 1")
    child2 = Leaf(Position(50, 90), info="Child 2")
    grandchild = Leaf(Position(15, 35), info="Grandchild")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild)

    print("Basic Tree:")
    tree.visualize()


def example_custom_visualization():
    """Demonstrate different visualization options."""
    tree = Tree("Visualization Example")
    root = Leaf(Position(0, 100), info="Root")
    child1 = Leaf(Position(10, 40), info="Child 1")
    child2 = Leaf(Position(50, 90), info="Child 2")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    print("\nDefault visualization:")
    tree.visualize()

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


def example_json_serialization():
    """Demonstrate JSON serialization."""
    # Create a simple tree
    tree = Tree("Serialization Example")
    root = Leaf(Position(0, 100), info="Root")
    child = Leaf(Position(10, 50), info="Child")
    tree.root = root
    tree.add_leaf(child)

    # Serialize to JSON
    json_str = tree.to_json()
    print("JSON representation:", json_str)

    # Deserialize from JSON
    loaded_tree = Tree.from_json(json_str)
    print("\nDeserialized tree:")
    loaded_tree.visualize()


def demonstrate_line_positions():
    print("\n=== Line Position Examples ===")

    # Create a tree with line numbers
    tree = Tree("Line Number Example")

    # Create root with line numbers
    root = Leaf(Position(0, 100), "Function")
    root.position.lineno = 1
    root.position.end_lineno = 10
    root.position.col_offset = 0
    root.position.end_col_offset = 4
    tree.root = root

    # Create a child node (if statement)
    if_node = Leaf(Position(20, 60), "If Block")
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


def demonstrate_dot_notation():
    print("\n=== Dot Notation Examples ===")
    # Create a tree structure
    root = Leaf(Position(0, 100), {"type": "Module"})
    child1 = Leaf(Position(10, 40), {"type": "FunctionDef", "name": "hello"})
    child2 = Leaf(Position(50, 90), {"type": "ClassDef", "name": "MyClass"})
    grandchild = Leaf(Position(20, 30), {"type": "Return"})

    # Build the tree
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    # Initialize attributes by calling _as_dict()
    root._as_dict()
    child1._as_dict()
    child2._as_dict()
    grandchild._as_dict()

    # Find parent using dot notation
    def safe_get_info(node):
        if not node or not hasattr(node, "attributes"):
            return {}
        attrs = getattr(node, "attributes", None)
        if not attrs:
            return {}
        info = getattr(attrs, "info", {})
        return info if isinstance(info, dict) else {}

    found_parent = grandchild.find_parent(lambda n: bool(n and n._as_dict(
    ) and safe_get_info(n).get("type") == "FunctionDef"))
    print("Parent:", safe_get_info(found_parent))

    # Find child using dot notation
    found_child = root.find_child(lambda n: bool(n and n._as_dict(
    ) and safe_get_info(n).get("type") == "ClassDef"))
    print("Child:", safe_get_info(found_child))

    # Find sibling using dot notation
    found_sibling = child1.find_sibling(lambda n: bool(n and n._as_dict(
    ) and safe_get_info(n).get("name") == "MyClass"))
    print("Sibling:", safe_get_info(found_sibling))


def demonstrate_ast_parsing():
    print("\n=== AST Examples ===")

    code = """
    class MyClass:
        def hello(self):
            return "world"
    """

    builder = AstTreeBuilder(code)
    tree = builder.build()
    if tree is None:
        print("Tree is None")
        return

    if tree.root is None:
        print("Tree root is None")
        return

    # Find class definition node
    class_node = tree.root.find(lambda n: (n is not None and hasattr(
        n, "info") and n.info is not None and isinstance(n.info, dict) and n.
                                           info.get("type") == "ClassDef"))
    print("=== AST Node Info Example ===")
    if class_node and hasattr(class_node, "ast_node") and class_node.ast_node:
        print(f"Class name: {class_node.ast_node.name}")
        print(f"Fields: {class_node.ast_node._fields}")
        print(f"Info dict: {class_node.info}")
    else:
        print("Class definition not found")


def demonstrate_node_navigation():
    """
    Demonstrates navigation between different types of
    nodes in the tree including top_statement.
    """
    # Create test nodes
    root = Leaf(Position(0, 100), "Root")
    child1 = Leaf(Position(10, 40), "Child 1")
    child2 = Leaf(Position(50, 90), "Child 2")

    # Build tree structure
    root.add_child(child1)
    root.add_child(child2)

    # Demonstrate navigation
    parent_info = child1.parent.info if child1.parent else None
    next_info = child1.next.info if child1.next else None
    prev_info = child2.previous.info if child2.previous else None

    print(f"Child 1's parent: {parent_info}")
    print(f"Child 1's next sibling: {next_info}")
    print(f"Child 2's previous sibling: {prev_info}")


def demonstrate_statements():
    """Demonstrates Statement functionality"""
    print("\n=== Statement Examples ===")

    # Basic statement
    part = PartStatement(before="print(", after=")")
    stmt = Statement(top=part, before="a.b.", self="d", after=".e")

    print("Default markers:")
    print(stmt.text)

    print("\nCustom markers:")
    print(stmt.as_text(top_marker="#", chain_marker="-", current_marker="@"))


def demonstrate_custom_root_visualization():
    """Demonstrate visualization from different root nodes."""
    tree = Tree("Custom Root Example")
    root = Leaf(Position(0, 100), info="Root")
    child = Leaf(Position(10, 50), info="Child")
    grandchild = Leaf(Position(20, 30), info="Grandchild")

    tree.root = root
    tree.add_leaf(child)
    child.add_child(grandchild)

    print("\nVisualize from Root:")
    tree.visualize()

    print("\nVisualize from Child:")
    tree.visualize(root=child)

    print("\nRich visualization from Child:")
    printer = RichTreePrinter()
    printer.print_tree(tree, root=child)


def run_demo():
    print("=== Tree Interval Package Demo ===")
    demonstrate_positions()
    demonstrate_leaves()
    demonstrate_tree_operations()
    example_basic_tree()
    example_custom_visualization()
    example_json_serialization()
    demonstrate_line_positions()
    demonstrate_dot_notation()
    demonstrate_ast_parsing()
    demonstrate_node_navigation()
    demonstrate_statements()
    demonstrate_custom_root_visualization()


if __name__ == "__main__":
    run_demo()
