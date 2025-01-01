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


if __name__ == "__main__":
    pytest.main([__file__])
