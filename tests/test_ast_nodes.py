
"""Tests for AST node information access"""
from typing import Optional

from tree_interval import AstTreeBuilder


def test_ast_node_access() -> None:
    code = "x = 1 + 2"
    builder = AstTreeBuilder(code)
    tree = builder.build()

    found_node = tree.root.find(lambda n: n.info.get("type") == "Assign")
    assert found_node is not None
    assert hasattr(found_node.ast_node, "targets")
    assert hasattr(found_node.ast_node, "value")


def test_ast_node_fields() -> None:
    code = "def test(): pass"
    builder = AstTreeBuilder(code)
    tree = builder.build()

    found_node = tree.root.find(lambda n: n.info.get("type") == "FunctionDef")
    assert found_node is not None
    assert "name" in found_node.ast_node._fields
    assert found_node.ast_node.name == "test"
