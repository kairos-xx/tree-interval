
"""Tests for frame analyzer functionality."""
import pytest
from src.tree_interval import FrameAnalyzer
import sys

def test_frame_analyzer_creation():
    frame = sys._getframe()
    analyzer = FrameAnalyzer(frame)
    assert analyzer.frame == frame
    assert analyzer.tree is None
    
def test_find_current_node():
    frame = sys._getframe()
    analyzer = FrameAnalyzer(frame)
    node = analyzer.find_current_node()
    assert node is not None
    
def test_build_tree():
    frame = sys._getframe() 
    analyzer = FrameAnalyzer(frame)
    tree = analyzer.build_tree()
    assert tree is not None
    assert tree.root is not None
