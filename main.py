"""
Tree Interval Package Demo - Comprehensive Examples
"""
from inspect import currentframe
from src.tree_interval import (
    AstTreeBuilder,
    FrameAnalyzer,
    Leaf,
    Position,
    Tree,
    TreeVisualizer,
    VisualizationConfig,
)


def demonstrate_basic_tree():
    """Basic tree creation and manipulation."""
    print("\n=== Basic Tree Example ===")
    tree = Tree("Basic Example")
    root = Leaf(0, 100, "Root")
    child1 = Leaf(10, 40, "Child 1")
    child2 = Leaf(50, 90, "Child 2")
    grandchild = Leaf(15, 35, "Grandchild")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild)

    print("Default visualization:")
    tree.visualize()

    print("\nWith position objects:")
    TreeVisualizer.visualize(tree,
                             VisualizationConfig(position_format="position"))

    print("\nWith tuples and children count:")
    TreeVisualizer.visualize(
        tree,
        VisualizationConfig(position_format="tuple",
                            show_children_count=True,
                            show_size=False))


def demonstrate_ast_analysis():
    """AST analysis example."""
    print("\n=== AST Analysis Example ===")
    code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
    """
    builder = AstTreeBuilder(code)
    ast_tree = builder.build()
    print("AST Tree visualization:")
    ast_tree.visualize()


def demonstrate_frame_analysis():
    """Frame analysis example."""
    print("\n=== Frame Analysis Example ===")

    def sample_function():
        x = 1
        y = 2
        z = x + y
        frame = currentframe()
        analyzer = FrameAnalyzer(frame)
        current_node = analyzer.find_current_node()
        if current_node:
            print("Current node in execution:")
            print(f"Position: {current_node.start}-{current_node.end}")
            print(f"Info: {current_node.info}")

    sample_function()


def demonstrate_serialization():
    """JSON serialization example."""
    print("\n=== Serialization Example ===")
    tree = Tree("Serialization Demo")
    root = Leaf(0, 100, "Root")
    child = Leaf(10, 50, "Child")
    tree.root = root
    tree.add_leaf(child)

    json_str = tree.to_json()
    print("JSON representation:", json_str)

    loaded_tree = Tree.from_json(json_str)
    print("\nDeserialized tree:")
    loaded_tree.visualize()


if __name__ == "__main__":
    demonstrate_basic_tree()
    demonstrate_ast_analysis()
    demonstrate_frame_analysis()
    demonstrate_serialization()
