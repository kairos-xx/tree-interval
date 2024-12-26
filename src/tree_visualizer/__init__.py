
"""
Tree Visualizer package.

A Python package for building and visualizing tree structures with support for AST analysis.
"""

from .core.tree_core import Tree, Leaf, Position
from .core.tree_visualizer import TreeVisualizer
from .config import VisualizationConfig
from .core.ast_tree_builder import AstTreeBuilder

__version__ = "0.1.0"
__all__ = [
    'Tree', 'Leaf', 'Position', 'TreeVisualizer', 'VisualizationConfig',
    'AstTreeBuilder'
]
