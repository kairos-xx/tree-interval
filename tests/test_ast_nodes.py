
"""Tests for AST node information access"""
import pytest
from tree_interval import AstTreeBuilder

def test_ast_node_access():
    code = "x = 1 + 2"
    builder = AstTreeBuilder(code)
    tree = builder.build()
    
    assign_node = tree.root.find(lambda n: n.info.get('type') == 'Assign')
    assert assign_node.ast_node is not None
    assert hasattr(assign_node.ast_node, 'targets')
    assert hasattr(assign_node.ast_node, 'value')

def test_ast_node_fields():
    code = "def test(): pass"
    builder = AstTreeBuilder(code)
    tree = builder.build()
    
    func_node = tree.root.find(lambda n: n.info.get('type') == 'FunctionDef')
    assert 'name' in func_node.ast_node._fields
    assert func_node.ast_node.name == 'test'
