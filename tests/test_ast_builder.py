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
        builder = AstTreeBuilder("")
        builder.build()


def test_ast_builder_malformed_ast():
    builder = AstTreeBuilder("invalid python code )")
    with pytest.raises(SyntaxError):
        builder.build()


def test_get_node_value_edge_cases():
    builder = AstTreeBuilder("x = 1")
    tree = builder.build()
    assert tree is not None


if __name__ == "__main__":
    pytest.main([__file__])

def test_invalid_source():
    with pytest.raises(ValueError):
        builder = AstTreeBuilder(None)
        builder.build()

def test_malformed_ast():
    builder = AstTreeBuilder("def invalid syntax:")
    with pytest.raises(SyntaxError):
        builder.build()

def test_empty_source():
    builder = AstTreeBuilder("")
    tree = builder.build()
    assert tree is not None

def test_get_node_value_edge_cases():
    builder = AstTreeBuilder("a[b]") # Test subscript
    tree = builder.build()
    assert tree is not None

def test_build_frame_edge_cases():
    builder = AstTreeBuilder("")
    assert builder.build_from_frame() is None
