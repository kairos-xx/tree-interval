"""
Tree Visualizer package.

A Python package for building and visualizing tree structures with support for AST analysis.
"""

from ..core.interval_core import Leaf, Tree
from .config import VisualizationConfig

DEFAULT_CONFIG = VisualizationConfig()


class TreeVisualizer:
    @staticmethod
    def visualize(tree, config: Optional[VisualizationConfig] = None):
        """Visualize a tree structure with customizable formatting options."""
        if config is None:
            config = DEFAULT_CONFIG

        if not tree.root:
            print("Empty tree")
            return

        def format_position(node) -> str:
            if config.position_format == "position":
                return (
                    f"Position(start={node.start}, end={node.end}, "
                    f"lineno={node.lineno}, end_lineno={node.end_lineno}, "
                    f"col_offset={node.col_offset}, end_col_offset={node.end_col_offset}, "
                    f"size={node.size})"
                )
            elif config.position_format == "tuple":
                return f"({node.start}, {node.end})"
            return f"[{node.start}, {node.end}]"

        def _print_node(node, level=0, prefix=""):
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

        print(f"Source: {tree.source}")
        _print_node(tree.root)


__version__ = "0.1.0"
__all__ = ["TreeVisualizer", "VisualizationConfig"]
