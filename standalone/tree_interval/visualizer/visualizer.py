"""Tree Visualization Core Module."""

from typing import Any, Optional

from tree_interval.visualizer.config import VisualizationConfig

DEFAULT_CONFIG = VisualizationConfig()


class TreeVisualizer:
    """Main class for visualizing tree structures."""

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    @staticmethod
    def visualize(
        tree: Any,
        config: Optional[VisualizationConfig] = None,
        root: Optional[Any] = None,
    ) -> None:
        """Visualize a tree structure with customizable formatting options."""
        if config is None:
            config = DEFAULT_CONFIG

        display_root = root if root is not None else tree.root
        if not display_root:
            print("Empty tree")
            return

        def format_position(node: Any) -> str:
            if config.position_format == "position":
                return (
                    f"Position(start={node.start}, end={node.end}, "
                    f"lineno={node.lineno}, end_lineno={node.end_lineno}, "
                    f"col_offset={node.col_offset}, "
                    f"end_col_offset={node.end_col_offset}, "
                    f"size={node.size})"
                )
            elif config.position_format == "tuple":
                return f"({node.start}, {node.end})"
            return f"({node.start}, {node.end})"

        def format_node_info(node: Any, level: int = 0, info_len: int = 0) -> str:
            parts: list[str] = []
            terminal_width = config.terminal_size
            available_width = terminal_width - info_len + ((level + 1) * 4) + 4
            if config.show_size:
                parts.append(f"size={node.size}")

            if config.show_info and node.info:
                if isinstance(node.info, dict):
                    info_str = (
                        "Info("
                        + ", ".join(f"{k}={repr(v)}" for k, v in node.info.items())
                        + ")"
                    )
                else:
                    info_str = repr(node.info)

                info_str = f"info={info_str}"

                current_length = len(" ".join(parts))
                remaining_width = available_width - current_length - 1
                if len(info_str) > remaining_width:
                    parts.append("info=...")
                else:
                    parts.append(info_str)

            if config.show_children_count:
                parts.append(f"children={len(node.children)}")

            return " ".join(parts)

        def _print_node(node: Any, prefix: str = "", is_last: bool = True, level: int = 0) -> None:
            position_str = format_position(node)

            prefix_spaces = "" if level < 2 else prefix
            connector = "" if level == 0 else ("└── " if is_last else "├── ")

            if hasattr(node, "style") and node.style:
                color = node.style.color.lstrip("#")
                style_prefix = (
                    f"\033[38;2;{int(color[:2], 16)};"
                    + f"{int(color[2:4], 16)};"
                    + f"{int(color[4:], 16)}m"
                )
                if node.style.bold:
                    style_prefix = "\033[1m" + style_prefix
            else:
                style_prefix = (
                    TreeVisualizer.BLUE
                    if level == 0
                    else (
                        TreeVisualizer.GREEN
                        if node.children
                        else TreeVisualizer.YELLOW
                    )
                )
            style_suffix = TreeVisualizer.RESET
            info_len = len(
                f"{prefix_spaces}{connector}{style_prefix}{position_str} "
                + f"{style_suffix}"
            )
            info_str = format_node_info(node, level, info_len)
            print(
                f"{prefix_spaces}{connector}{style_prefix}{position_str} "
                + f"{info_str}{style_suffix}"
            )
            children = node.children
            for i, child in enumerate(children):
                new_prefix = prefix + ("    " if is_last else "│   ")
                _print_node(child, new_prefix, i == len(children) - 1, level + 1)

        _print_node(display_root)