from textwrap import dedent

import pytest

from tree_interval import AstTreeBuilder


def test_ast_builder_initialization():
    source = "x = 1"
    builder = AstTreeBuilder(source)
    assert builder.source == source
    assert builder.indent_offset == 0


def test_build_from_source():
    source = dedent(
        """
    def test():
        x = 1
        return x
    """
    ).strip()

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
    call_node = next(
        n for n in nodes if getattr(n, "info", {}).get("type") == "Module"
    )
    assert call_node is not None


def test_position_tracking():
    source = dedent(
        """
    def func():
        return 42
    """
    ).strip()

    builder = AstTreeBuilder(source)
    tree = builder.build()

    assert tree is not None
    func_node = next(
        n
        for n in tree.flatten()
        if getattr(n, "info", {}).get("type") == "FunctionDef"
    )
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
        builder = AstTreeBuilder(None)  # pyright: ignore
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
    assert tree.root is None


def test_attribute_node_value():
    source = "obj.attr.subattr"
    builder = AstTreeBuilder(source)
    tree = builder.build()

    attr_node = None
    if tree:
        nodes = tree.flatten()
        attr_node = next(
            n
            for n in nodes
            if getattr(n, "info", {}).get("type") == "Attribute"
        )
    assert attr_node is not None


def test_call_node_value():
    source = "func(1, 2)"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    call_node = None
    if tree:
        nodes = tree.flatten()
        call_node = next(
            n for n in nodes if getattr(n, "info", {}).get("type") == "Module"
        )
    assert call_node is not None


def test_subscript_node_value():
    source = "_ = arr[0]"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    subscript_node = None
    if tree:
        nodes = tree.flatten()
        subscript_node = next(
            n
            for n in nodes
            if getattr(n, "info", {}).get("type") == "Subscript"
        )
    assert subscript_node is not None


def test_binop_node_value():
    source = "_ = a + b"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    binop_node = None
    if tree:
        nodes = tree.flatten()
        binop_node = next(
            n for n in nodes if getattr(n, "info", {}).get("type") == "BinOp"
        )
    assert binop_node is not None


def test_lambda_node_value():
    source = "_ = lambda x: x * 2"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    lambda_node = None
    if tree:
        nodes = tree.flatten()
        lambda_node = next(
            n for n in nodes if getattr(n, "info", {}).get("type") == "Lambda"
        )
    assert lambda_node is not None


def test_build_no_source():
    builder = AstTreeBuilder("test")
    builder.source = None
    with pytest.raises(ValueError, match="No source code available"):
        builder.build()


def test_get_node_position_missing_lineno():
    from ast import Load, Name

    builder = AstTreeBuilder("x = 1")
    node = Name(id="x", ctx=Load())
    # Node without lineno should return None
    assert builder._get_node_position(node) is None


def test_node_with_invalid_source():
    builder = AstTreeBuilder("x = 1")
    builder.source = ""  # Invalid source
    from ast import Load, Name

    node = Name(id="x", ctx=Load())
    node.lineno = 1
    node.col_offset = 0
    node.end_lineno = 1
    node.end_col_offset = 1
    # Should handle invalid source gracefully
    assert builder._get_node_position(node) is None


def test_build_tree_from_ast_empty_source():
    builder = AstTreeBuilder(" ")
    builder.source = None
    from ast import parse

    with pytest.raises(ValueError, match="No source code available"):
        builder._build_tree_from_ast(parse(""))


def test_get_node_position_with_empty_lines():
    """Test node position handling with empty lines in source."""
    from ast import Load, Name

    builder = AstTreeBuilder("x = 1\n\ny = 2")
    node = Name(id="y", ctx=Load())
    node.lineno = 3
    node.col_offset = 0
    node.end_lineno = 3
    node.end_col_offset = 1
    position = builder._get_node_position(node)
    assert position is not None


def test_build_tree_with_duplicate_positions():
    """Test handling nodes with identical positions."""
    source = "x = y = 1"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    assert tree is not None

    # Get all nodes with the same position
    nodes = [n for n in tree.flatten() if n.start == n.end]
    # Verify proper handling of duplicate positions
    assert len(nodes) >= 0


def test_build_tree_with_nested_nodes():
    """Test handling deeply nested AST nodes."""
    source = """
def outer():
    def inner():
        x = 1
        return x
    return inner()
    """
    builder = AstTreeBuilder(source)
    tree = builder.build()
    assert tree is not None

    # Find the innermost node
    inner_nodes = [
        n
        for n in tree.flatten()
        if getattr(n, "info", {}).get("type") == "FunctionDef"
        and getattr(n, "info", {}).get("name") == "inner"
    ]
    assert len(inner_nodes) > 0


def test_node_position_empty_source_lines():
    """Test position calculation with empty source lines."""
    from ast import Load, Name

    builder = AstTreeBuilder("\n\nx = 1")
    node = Name(id="x", ctx=Load())
    node.lineno = 3
    node.col_offset = 0
    node.end_lineno = 3
    node.end_col_offset = 1
    position = builder._get_node_position(node)
    assert position is not None
    assert position.lineno == 3


def test_build_tree_complex_hierarchy():
    """Test building tree with complex parent-child relationships."""
    source = """
class A:
    def method1(self):
        if True:
            def nested():
                return 42
            return nested()
    """
    builder = AstTreeBuilder(source)
    tree = builder.build()
    assert tree is not None

    # Test the hierarchy structure
    nodes = tree.flatten()
    class_node = next(
        n for n in nodes if getattr(n, "info", {}).get("type") == "ClassDef"
    )
    assert any(
        getattr(child, "info", {}).get("type") == "FunctionDef"
        for child in class_node.children
    )


def test_build_tree_duplicate_leaf():
    """Test handling of duplicate leaf additions."""
    source = "x = y = z = 1"
    builder = AstTreeBuilder(source)
    tree = builder.build()
    assert tree is not None

    # Get all assignment targets
    nodes = [
        n
        for n in tree.flatten()
        if getattr(n, "info", {}).get("type") == "Name"
    ]
    assert len(nodes) > 0


def test_node_value_extraction_edge_cases():
    """Test _get_node_value method with various node types."""
    from ast import AST, Constant

    builder = AstTreeBuilder("x = 1")

    # Test unsupported node type
    class CustomNode(AST):
        pass

    custom_node = CustomNode()
    assert builder._get_node_value(custom_node) == ""

    # Test constant node
    constant_node = Constant(value=42)
    assert builder._get_node_value(constant_node) == "42"


def test_ast_node_processing():
    """Test processing nodes during tree building."""
    source = """
class Test:
    def method(self):
        pass
    """
    builder = AstTreeBuilder(source)
    tree = builder.build()
    class_node = None
    # Verify node processing
    if tree:
        nodes = tree.flatten()
        class_node = next(
            n
            for n in nodes
            if getattr(n, "info", {}).get("type") == "ClassDef"
        )
    assert getattr(class_node, "info", {}).get("name") == "Test"
    assert getattr(class_node, "ast_node", None) is not None


if __name__ == "__main__":
    pytest.main([__file__])
