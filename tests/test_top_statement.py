
"""Tests for top_statement property"""

from tree_interval import Leaf, Position, Tree

def test_top_statement_basic():
    """Test basic top_statement functionality"""
    # Create a simple assignment: x = 1
    tree = Tree("Test")
    assign = Leaf(Position(0, 10), {"type": "Assign"})
    name = Leaf(Position(2, 8), {"type": "Name"})
    
    tree.root = assign
    assign.add_child(name)
    
    assert name.top_statement == assign
    assert assign.top_statement == assign

def test_top_statement_complex():
    """Test top_statement with complex expressions"""
    # Create: result = obj.method().value
    assign = Leaf(Position(0, 30), {"type": "Assign"})
    call = Leaf(Position(10, 25), {"type": "Call"})
    attr1 = Leaf(Position(12, 20), {"type": "Attribute"})
    attr2 = Leaf(Position(15, 18), {"type": "Attribute"})
    
    assign.add_child(call)
    call.add_child(attr1)
    attr1.add_child(attr2)
    
    assert attr2.top_statement == assign
    assert attr1.top_statement == assign
    assert call.top_statement == assign
