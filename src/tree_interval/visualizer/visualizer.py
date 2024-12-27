<<<<<<< HEAD

=======
>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
"""
Tree Visualizer package.

A Python package for building and visualizing tree structures
with support for AST analysis.
"""

from typing import Optional
<<<<<<< HEAD
=======

>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
from .config import VisualizationConfig

DEFAULT_CONFIG = VisualizationConfig()

<<<<<<< HEAD
class TreeVisualizer:
    # ANSI color codes
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

=======

class TreeVisualizer:
>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
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
                    f"col_offset={node.col_offset}, "
<<<<<<< HEAD
                    f"end_col_offset={node.end_col_offset}, "
=======
                    + f"end_col_offset={node.end_col_offset}, "
>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
                    f"size={node.size})"
                )
            elif config.position_format == "tuple":
                return f"({node.start}, {node.end})"
<<<<<<< HEAD
            return f"({node.start}, {node.end})"

        def format_node_info(node) -> str:
            parts = []
=======
            return f"[{node.start}, {node.end}]"

        def _print_node(node, level=0, prefix=""):
            indent = "    " * level
            parts = [f"{indent}{prefix}{format_position(node)}"]

>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
            if config.show_size:
                parts.append(f"size={node.size}")
            if config.show_info and node.info:
                parts.append(f"info='{node.info}'")
            if config.show_children_count:
                parts.append(f"children={len(node.children)}")
<<<<<<< HEAD
            return " ".join(parts)

        def _print_node(node, prefix="", is_last=True, level=0):
            position_str = format_position(node)
            info_str = format_node_info(node)
            prefix_spaces = "    " if level == 0 else prefix
            connector = "┌── " if level == 0 else ("└── " if is_last else "├── ")
            
            # Color the text content but not the tree lines
            color = TreeVisualizer.BLUE if level == 0 else (TreeVisualizer.GREEN if node.children else TreeVisualizer.YELLOW)
            print(f"{prefix_spaces}{connector}{color}{position_str} {info_str}{TreeVisualizer.RESET}")

            children = node.children
            for i, child in enumerate(children):
                new_prefix = prefix + ("    " if is_last else "│   ")
                _print_node(child, new_prefix, i == len(children) - 1, level + 1)

        _print_node(tree.root)

=======

            print(" ".join(parts))

            for i, child in enumerate(node.children):
                is_last = i == len(node.children) - 1
                _print_node(child, level + 1, "└── " if is_last else "├── ")

        print(f"Source: {tree.source}")
        _print_node(tree.root)


>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
__version__ = "0.1.0"
__all__ = ["TreeVisualizer", "VisualizationConfig"]
