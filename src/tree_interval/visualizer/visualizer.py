"""
Tree Visualizer package.

A Python package for building and visualizing tree structures
with support for AST analysis.
"""

from typing import Optional

from .config import VisualizationConfig

DEFAULT_CONFIG = VisualizationConfig()


class TreeVisualizer:
    # ANSI color codes
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

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
                return (f"Position(start={node.start}, end={node.end}, "
                        f"lineno={node.lineno}, end_lineno={node.end_lineno}, "
                        f"col_offset={node.col_offset}, "
                        f"end_col_offset={node.end_col_offset}, "
                        f"size={node.size})")
            elif config.position_format == "tuple":
                return f"({node.start}, {node.end})"
            return f"({node.start}, {node.end})"

        def get_terminal_width() -> int:
            try:
                import shutil

                columns, _ = shutil.get_terminal_size()
                return columns
            except Exception:
                return 80  # Default fallback width

        def format_node_info(node, level: int = 0) -> str:
            parts = []
            prefix_len = level * 4 + 4  # Basic indentation + connector length
            terminal_width = get_terminal_width()
            available_width = terminal_width - prefix_len

            if config.show_size:
                parts.append(f"size={node.size}")

            if config.show_info and node.info:
                if isinstance(node.info, dict):
                    info_str = ("Info(" +
                                ", ".join(f"{k}={repr(v)}"
                                          for k, v in node.info.items()) + ")")
                else:
                    info_str = repr(node.info)

                # Calculate total length including existing parts
                current_length = len(" ".join(parts))
                remaining_width = available_width - current_length - 1
                # -1 for space

                if len(info_str) > remaining_width:
                    parts.append("info=...")
                else:
                    parts.append(info_str if isinstance(node.info, dict) else
                                 f"info={info_str}")

            if config.show_children_count:
                parts.append(f"children={len(node.children)}")

            return " ".join(parts)

        def _print_node(node, prefix="", is_last=True, level=0):
            position_str = format_position(node)
            info_str = format_node_info(node)
            prefix_spaces = "" if level == 0 else prefix
            connector = "" if level == 0 else ("└── " if is_last else "├── ")

            # Custom styling takes precedence
            if hasattr(node, 'style') and node.style:
                color = node.style.color.lstrip('#')
                style_prefix = (f"\033[38;2;{int(color[:2], 16)};" +
                                f"{int(color[2:4], 16)};" +
                                f"{int(color[4:], 16)}m")
                if node.style.bold:
                    style_prefix = "\033[1m" + style_prefix
            else:
                # Default styling
                style_prefix = TreeVisualizer.BLUE if level == 0 else (
                    TreeVisualizer.GREEN
                    if node.children else TreeVisualizer.YELLOW)
            style_suffix = TreeVisualizer.RESET

            print(f"{prefix_spaces}{connector}{style_prefix}{position_str} " +
                  f"{info_str}{style_suffix}")

            children = node.children
            for i, child in enumerate(children):
                new_prefix = prefix + ("    " if is_last else "│   ")
                _print_node(child, new_prefix, i == len(children) - 1,
                            level + 1)

        _print_node(tree.root)


__version__ = "0.1.0"
__all__ = ["TreeVisualizer", "VisualizationConfig"]
