
import pytest
from inspect import currentframe

from src.tree_interval import FrameAnalyzer

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
