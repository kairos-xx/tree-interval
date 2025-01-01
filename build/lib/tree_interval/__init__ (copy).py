"""
Tree Interval Package Root Module.

This package provides tools for analyzing and visualizing tree structures
with interval-based position tracking. It combines AST analysis, runtime
frame inspection, and rich visualization capabilities.

Key Components:
    - Core data structures (Tree, Leaf, Position)
    - AST analysis tools (AstTreeBuilder)
    - Frame analysis (FrameAnalyzer)
    - Visualization utilities (TreeVisualizer)

Usage:
    from tree_interval import Tree, Leaf, Position
    from tree_interval import FrameAnalyzer, AstTreeBuilder
    from tree_interval import TreeVisualizer, VisualizationConfig
"""

from .core.ast_builder import AstTreeBuilder
from .core.frame_analyzer import FrameAnalyzer
from .core.interval_core import Leaf, LeafStyle, Position, Tree
from .visualizer.visualizer import TreeVisualizer, VisualizationConfig

__all__ = [
    "Tree",
    "Leaf",
    "Position",
    "LeafStyle",
    "FrameAnalyzer",
    "AstTreeBuilder",
    "TreeVisualizer",
    "VisualizationConfig",
]

__version__ = '0.1.0'
