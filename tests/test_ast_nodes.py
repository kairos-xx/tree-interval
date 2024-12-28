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
