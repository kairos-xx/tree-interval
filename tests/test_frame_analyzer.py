from inspect import stack

import pytest

from tree_interval import FrameAnalyzer
from tree_interval.core.interval_core import Leaf, Position, Tree


def test_frame_analyzer_initialization():
    frame = stack()[0].frame
    analyzer = FrameAnalyzer(frame)
    assert analyzer.frame == frame
    assert analyzer.frame_position is not None


def test_build_tree():
    def sample_func():
        frame = stack()[0].frame
        analyzer = FrameAnalyzer(frame)
        return analyzer.build_tree()

    tree = sample_func()
    assert tree is not None
    assert tree.root is not None


def test_find_current_node():
    def another_func():
        frame = stack()[0].frame
        analyzer = FrameAnalyzer(frame)
        return analyzer.find_current_node()

    node = another_func()
    assert node is not None
    assert node.info is not None


def test_frame_analyzer_with_empty_frame():
    frame = stack()[0].frame
    analyzer = FrameAnalyzer(frame)
    analyzer.tree = None
    result = analyzer.find_current_node()
    assert isinstance(result, Leaf)


def test_frame_analyzer_position_handling():
    """Test frame position handling when frame is None"""
    analyzer = FrameAnalyzer(None)
    assert analyzer.frame_position.start == 0
    assert analyzer.frame_position.end == 0

    frame = stack()[0].frame
    analyzer = FrameAnalyzer(frame)
    assert analyzer.frame_position is not None
    assert analyzer.frame_position.start is not None
    assert analyzer.frame_position.end is not None


def test_frame_analyzer_empty_source():
    frame = stack()[0].frame
    analyzer = FrameAnalyzer(frame)
    if analyzer.ast_builder:
        analyzer.ast_builder.source = ""
    result = analyzer.build_tree()
    assert isinstance(result, Tree)


def test_frame_analyzer_invalid_frame():
    def nested_func():
        frame = stack()[0].frame
        analyzer = FrameAnalyzer(frame)
        analyzer.frame = None
        return analyzer.find_current_node()

    assert isinstance(nested_func(), Leaf)


def test_frame_analyzer_no_matching_position():
    def nested_func():
        frame = stack()[0].frame
        analyzer = FrameAnalyzer(frame)
        analyzer.frame_position.start = 999999
        analyzer.frame_position.end = 999999
        return analyzer.find_current_node()

    assert isinstance(nested_func(), Leaf)


def test_no_matching_nodes():
    def dummy_func():
        frame = stack()[0].frame
        analyzer = FrameAnalyzer(frame)
        analyzer.tree = Tree("")
        return analyzer.find_current_node()

    assert dummy_func() is None


def test_build_tree_empty():
    def dummy_func():
        frame = stack()[0].frame
        analyzer = FrameAnalyzer(frame)
        if analyzer.ast_builder:
            analyzer.ast_builder.source = None
        with pytest.raises(ValueError, match="No source code available"):
            return analyzer.build_tree()

    assert dummy_func() is None


def test_frame_analyzer_no_ast_node():
    def dummy_func():
        frame = stack()[0].frame
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
        frame = stack()[0].frame
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


def test_frame_analyzer_missing_tree():
    """Test frame analyzer when tree is missing"""
    from tree_interval import FrameAnalyzer

    analyzer = FrameAnalyzer(None)
    analyzer.tree = None
    result = analyzer.find_current_node()
    assert result is None


def test_frame_analyzer_no_matching_nodes_empty():
    """Test frame analyzer when no nodes match position"""
    from tree_interval import FrameAnalyzer, Leaf, Position, Tree

    analyzer = FrameAnalyzer(None)
    analyzer.tree = Tree("test")
    analyzer.tree.root = Leaf(Position(0, 10))
    # Set frame position that won't match any nodes
    analyzer.frame_position = Position(100, 200)
    result = analyzer.find_current_node()
    assert result is analyzer.tree.root


def test_node_matching_and_selection():
    """Test node matching and selection in frame analyzer"""
    from tree_interval import Leaf, Position, Tree
    from tree_interval.core.frame_analyzer import FrameAnalyzer

    # Create a basic tree with nodes
    tree = Tree("test")
    node1 = Leaf(Position(10, 50), info={"type": "Call", "name": "test"})
    node2 = Leaf(Position(10, 50), info={"type": "Call", "name": "test"})
    tree.root = node1

    # Initialize analyzer with the tree
    analyzer = FrameAnalyzer(None)
    analyzer.tree = tree
    analyzer.current_node = node2

    # Test matching and selection
    assert node1.match(analyzer.current_node)
    node1.selected = True
    assert node1.selected


if __name__ == "__main__":
    pytest.main([__file__])
