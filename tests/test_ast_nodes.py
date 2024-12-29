"""Tests for AST node information access"""

from tree_interval import AstTreeBuilder


def test_ast_node_access() -> None:
    code = "x = 1 + 2"
    builder = AstTreeBuilder(code)
    tree = builder.build()
    if tree is None:
        raise AssertionError("Tree is None")
    if tree.root is None:
        raise AssertionError("Tree root is None")

    found_node = tree.root.find(
        lambda n: (n.info is not None and n.info.get("type") == "Assign")
    )
    if not found_node or not found_node.ast_node:
        raise AssertionError("Node not found or ast_node is None")
    assert hasattr(found_node.ast_node, "targets")
    assert hasattr(found_node.ast_node, "value")


def test_ast_node_fields() -> None:
    code = "def test(): pass"
    builder = AstTreeBuilder(code)
    tree = builder.build()
    if tree is None:
        raise AssertionError("Tree is None")
    if tree.root is None:
        raise AssertionError("Tree root is None")

    found_node = tree.root.find(
        lambda n: (n.info is not None and n.info.get("type") == "FunctionDef")
    )
    if not found_node or not found_node.ast_node:
        raise AssertionError("Node not found or ast_node is None")
    assert "_fields" in dir(found_node.ast_node)
    assert "name" in found_node.ast_node._fields
    assert found_node.ast_node.name == "test"


def test_top_statement_basic() -> None:
    """Test basic top_statement functionality"""
    # Create a simple assignment: x = 1
    tree = Tree("Test")
    assign = Leaf(Position(0, 10), {"type": "Assign"})
    name = Leaf(Position(2, 8), {"type": "Name"})
    
    tree.root = assign
    assign.add_child(name)
    
    assert name.top_statement == assign
    assert assign.top_statement == assign


def test_top_statement_complex() -> None:
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
