
"""Tree Interval Package.

A Python package for managing and visualizing interval tree structures.
Provides tools for creating, manipulating and visualizing tree structures
with interval-based positions.
"""

from .core.interval_core import Tree, Leaf, Position
from src.tree_visualizer import TreeVisualizer, VisualizationConfig
from .core.ast_builder import AstTreeBuilder

__version__ = "0.1.0"
__all__ = [
    'Tree', 'Leaf', 'Position',
    'TreeVisualizer', 'VisualizationConfig',
    'AstTreeBuilder'
]
