from inspect import currentframe

import pytest

from tree_interval import FrameAnalyzer
from tree_interval.core.interval_core import Leaf, Position, Tree


def test_frame_analyzer_initialization():
    frame = currentframe()
    analyzer = FrameAnalyzer(frame)
    assert analyzer.frame == frame
    assert analyzer.frame_position is not None


def test_build_tree():

    def sample_func():
        frame = currentframe()
        analyzer = FrameAnalyzer(frame)
        return analyzer.build_tree()

    tree = sample_func()
    assert tree is not None
    assert tree.root is not None


def test_find_current_node():

    def another_func():
        frame = currentframe()
        analyzer = FrameAnalyzer(frame)
        return analyzer.find_current_node()

    node = another_func()
    assert node is not None
    assert node.info is not None


def test_empty_frame():
    frame = None
    with pytest.raises(ValueError):
        _ = FrameAnalyzer(frame)


def test_frame_analyzer_with_empty_frame():
    frame = currentframe()
    analyzer = FrameAnalyzer(frame)
    analyzer.tree = None
    result = analyzer.find_current_node()
    assert isinstance(result, Leaf)


def test_frame_analyzer_empty_source():
    frame = currentframe()
    analyzer = FrameAnalyzer(frame)
    analyzer.ast_builder.source = ""
    result = analyzer.build_tree()
    assert result is None


def test_frame_analyzer_invalid_frame():

    def nested_func():
        frame = currentframe()
        analyzer = FrameAnalyzer(frame)
        analyzer.frame = None
        return analyzer.find_current_node()

    assert isinstance(nested_func(), Leaf)


def test_frame_analyzer_no_matching_position():

    def nested_func():
        frame = currentframe()
        analyzer = FrameAnalyzer(frame)
        analyzer.frame_position.start = 999999
        analyzer.frame_position.end = 999999
        return analyzer.find_current_node()

    assert isinstance(nested_func(), Leaf)


def test_no_matching_nodes():

    def dummy_func():
        frame = currentframe()
        analyzer = FrameAnalyzer(frame)
        analyzer.tree = Tree("")
        return analyzer.find_current_node()

    assert dummy_func() is None


def test_build_tree_empty():

    def dummy_func():
        frame = currentframe()
        analyzer = FrameAnalyzer(frame)
        analyzer.ast_builder.source = None
        return analyzer.build_tree()

    assert dummy_func() is None


def test_frame_analyzer_no_ast_node():
    def dummy_func():
        frame = currentframe()
        analyzer = FrameAnalyzer(frame)
        # Create a tree with nodes that don't have ast_node attribute
        analyzer.tree = Tree("")
        root = Leaf(Position(0, 100), info="root")
        analyzer.tree.root = root
        return analyzer.build_tree()

    result = dummy_func()
    assert isinstance(result, Tree)
    assert result.root is not None


def test_frame_analyzer_invalid_ast_node():
    def dummy_func():
        frame = currentframe()
        analyzer = FrameAnalyzer(frame)
        analyzer.tree = Tree("")
        root = Leaf(Position(0, 100), info="root")
        # Set invalid ast_node
        root.ast_node = "not an AST node"
        analyzer.tree.root = root
        return analyzer.build_tree()

    result = dummy_func()
    assert isinstance(result, Tree)
    assert result.root is not None

def test_build_tree_no_current_node():
    """Test building tree with no current node."""
    frame_analyzer = FrameAnalyzer(None)
    frame_analyzer.tree = Tree("test")
    frame_analyzer._find_node_positions()
    assert frame_analyzer.current_node is None

def test_build_tree_with_ast():
    """Test building tree with AST nodes."""
    import ast
    node = ast.Name(id='x', ctx=ast.Load())
    frame_analyzer = FrameAnalyzer(None)
    frame_analyzer.tree = Tree("x = 1")
    leaf = Leaf(Position(0, 1))
    leaf.ast_node = node
    frame_analyzer.tree.root = leaf
    result = frame_analyzer.build_tree()
    assert result is not None


if __name__ == "__main__":
    pytest.main([__file__])