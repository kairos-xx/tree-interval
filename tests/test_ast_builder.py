from textwrap import dedent

import pytest

from tree_interval import AstTreeBuilder


def test_ast_builder_initialization():
    source = "x = 1"
    builder = AstTreeBuilder(source)
    assert builder.source == source
    assert builder.indent_offset == 0


def test_build_from_source():
    source = dedent("""
    def test():
        x = 1
        return x
    """).strip()

    builder = AstTreeBuilder(source)
    tree = builder.build()

    assert tree is not None
    assert tree.root is not None
    assert isinstance(tree.root.info, dict)
    assert tree.root.info.get("type") == "Module"


def test_node_value_extraction():
    source = "x.y.z(1 + 2)"
    builder = AstTreeBuilder(source)
    tree = builder.build()

    assert tree is not None
    nodes = tree.flatten()
    call_node = next(n for n in nodes
                     if getattr(n, "info", {}).get("type") == "Call")
    assert call_node is not None


def test_position_tracking():
    source = dedent("""
    def func():
        return 42
    """).strip()

    builder = AstTreeBuilder(source)
    tree = builder.build()

    assert tree is not None
    func_node = next(n for n in tree.flatten()
                     if getattr(n, "info", {}).get("type") == "FunctionDef")
    assert func_node.position.lineno == 1
    assert func_node.position.end_lineno == 2


def test_ast_builder_invalid_source():
    with pytest.raises(ValueError):
        _ = AstTreeBuilder("")


def test_ast_builder_malformed_ast():
    builder = AstTreeBuilder("invalid python code )")
    with pytest.raises(SyntaxError):
        builder.build()


def test_get_node_value_edge_cases():
    builder = AstTreeBuilder("x = 1")
    tree = builder.build()
    assert tree is not None


def test_invalid_source():
    with pytest.raises(ValueError):
        builder = AstTreeBuilder(None)
        builder.build()


def test_malformed_ast():
    builder = AstTreeBuilder("def invalid syntax:")
    with pytest.raises(SyntaxError):
        builder.build()


def test_empty_source():
    with pytest.raises(ValueError):
        _ = AstTreeBuilder("")


def test_build_with_empty_string():
    builder = AstTreeBuilder(" ")
    tree = builder.build()
    assert tree is not None
    assert isinstance(tree.root, Leaf)
    assert tree.root.info == ""

def test_attribute_node_value():
    source = "obj.attr.subattr"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    nodes = tree.flatten()
    attr_node = next(n for n in nodes if getattr(n, "info", {}).get("type") == "Attribute")
    assert attr_node is not None

def test_call_node_value():
    source = "func(1, 2)"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    nodes = tree.flatten()
    call_node = next(n for n in nodes if getattr(n, "info", {}).get("type") == "Call")
    assert call_node is not None

def test_subscript_node_value():
    source = "arr[0]"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    nodes = tree.flatten()
    subscript_node = next(n for n in nodes if getattr(n, "info", {}).get("type") == "Subscript")
    assert subscript_node is not None

def test_binop_node_value():
    source = "a + b"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    nodes = tree.flatten()
    binop_node = next(n for n in nodes if getattr(n, "info", {}).get("type") == "BinOp")
    assert binop_node is not None

def test_lambda_node_value():
    source = "lambda x: x * 2"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    nodes = tree.flatten()
    lambda_node = next(n for n in nodes if getattr(n, "info", {}).get("type") == "Lambda")
    assert lambda_node is not None



if __name__ == "__main__":
    pytest.main([__file__])
