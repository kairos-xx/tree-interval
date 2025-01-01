from inspect import currentframe

import pytest

from tree_interval import FrameAnalyzer
from tree_interval.core.interval_core import Tree


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
    analyzer = FrameAnalyzer(frame)
    assert analyzer.find_current_node() is None


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


if __name__ == "__main__":
    pytest.main([__file__])
