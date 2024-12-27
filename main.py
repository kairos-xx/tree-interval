
from src.tree_interval import Tree, Leaf, Position

def demonstrate_nested_attributes():
    """Example showing nested attribute access"""
    tree = Tree("Nested Attributes Example")
    root = Leaf(Position(0, 100, "Root Node"))
    child = Leaf(Position(10, 50, "Child Node"))
    
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

if __name__ == "__main__":
    demonstrate_nested_attributes()
