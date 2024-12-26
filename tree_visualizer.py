
"""
Tree Visualizer module.

This module provides utilities for visualizing tree structures with various
configuration options for display format and content.
"""

from dataclasses import dataclass
from typing import Optional

from tree_core import Leaf, Tree


@dataclass
class VisualizationConfig:
    """Configuration for tree visualization.
    
    Attributes:
        show_info: Whether to display node information
        show_size: Whether to display node sizes
        show_children_count: Whether to display number of children
        position_format: Format for position display ('range', 'position', or 'tuple')
    """
    show_info: bool = True
    show_size: bool = True
    show_children_count: bool = False
    position_format: str = 'range'  # 'range', 'position', or 'tuple'


DEFAULT_CONFIG = VisualizationConfig()


class TreeVisualizer:
    """Utility class for tree visualization with configurable display options."""

    @staticmethod
    def visualize(tree: Tree,
                  config: Optional[VisualizationConfig] = None) -> None:
        """Visualize a tree structure with customizable formatting options.
        
        Args:
            tree: The tree structure to visualize
            config: Configuration options for visualization
        """
        if config is None:
            config = DEFAULT_CONFIG

        if not tree.root:
            print("Empty tree")
            return

        def format_position(node: Leaf) -> str:
            if config.position_format == 'position':
                if hasattr(node, 'lineno'):
                    return (f"Position(lineno={node.lineno}, " +
                            f"end_lineno={node.end_lineno}, " +
                            f"col_offset={node.col_offset}, " +
                            f"end_col_offset={node.end_col_offset})")
                return f"Position(start={node.start or 'None'}, end={node.end or 'None'}, info='{node.info or 'None'}')"
            elif config.position_format == 'tuple':
                return f"({node.start}, {node.end})"
            return f"[{node.start}, {node.end}]"

        def _print_node(node: Leaf,
                        level: int = 0,
                        prefix: str = "") -> None:
            indent = "    " * level
            parts = [f"{indent}{prefix}{format_position(node)}"]

            if config.show_size:
                parts.append(f"size={node.size}")
            if config.show_info and node.info:
                parts.append(f"info='{node.info}'")
            if config.show_children_count:
                parts.append(f"children={len(node.children)}")

            print(" ".join(parts))

            for i, child in enumerate(node.children):
                is_last = i == len(node.children) - 1
                _print_node(child, level + 1, "└── " if is_last else "├── ")

        _print_node(tree.root)
