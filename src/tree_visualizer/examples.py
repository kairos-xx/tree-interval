
from tree_visualizer import Tree, Leaf, TreeVisualizer, VisualizationConfig, AstTreeBuilder
from inspect import currentframe

def example_basic_tree():
    """Basic tree creation and visualization example"""
    tree = Tree[str]("Example code")
    root = Leaf(0, 100, "root")
    child1 = Leaf(10, 40, "child1")
    child2 = Leaf(50, 90, "child2")
    
    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    
    print("Basic Tree Visualization:")
    tree.visualize()

def example_ast_analysis():
    """AST analysis example"""
    frame = currentframe()
    builder = AstTreeBuilder(frame)
    ast_tree = builder.build()
    
    print("\nAST Tree Analysis:")
    ast_tree.visualize()

if __name__ == "__main__":
    example_basic_tree()
    example_ast_analysis()
