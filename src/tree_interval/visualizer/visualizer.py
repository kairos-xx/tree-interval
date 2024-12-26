
"""Tree visualization module."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class VisualizationConfig:
    """Configuration for tree visualization."""
    show_info: bool = True
    show_size: bool = True
    show_children_count: bool = False
    position_format: str = 'range'  # 'range', 'position', or 'tuple'

class TreeVisualizer:
    @staticmethod
    def visualize(tree, config: Optional[VisualizationConfig] = None):
        if config is None:
            config = VisualizationConfig()

        if not tree.root:
            print("Empty tree")
            return

        def format_position(node) -> str:
            if config.position_format == 'position':
                return (f"Position(start={node.start}, end={node.end}, "
                       f"lineno={node.lineno}, end_lineno={node.end_lineno}, "
                       f"col_offset={node.col_offset}, end_col_offset={node.end_col_offset}, "
                       f"size={node.size})")
            elif config.position_format == 'tuple':
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
