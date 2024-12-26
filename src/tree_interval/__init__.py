
"""
Tree Interval package.

A Python package for managing and visualizing interval tree structures.
"""

from .core.interval_core import IntervalTree, IntervalNode, Position
from .core.visualizer import TreeVisualizer, VisualizationConfig
from .core.ast_builder import AstIntervalBuilder

__version__ = "0.1.0"
__all__ = [
    'IntervalTree', 'IntervalNode', 'Position', 'TreeVisualizer', 'VisualizationConfig',
    'AstIntervalBuilder'
]
