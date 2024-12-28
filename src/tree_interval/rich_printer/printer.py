"""Rich-based tree printer implementation."""

from typing import Optional

from rich.console import Console
from rich.tree import Tree as RichTree

from ..core.interval_core import Leaf, Tree
from .config import RichPrintConfig


class RichTreePrinter:
    """Prints tree structures using Rich library."""

    def __init__(
        self,
        config: Optional[RichPrintConfig] = None,
        console: Optional[Console] = None,
    ):
        self.config = config or RichPrintConfig()
        self.console = console or Console()

    def print_tree(self, tree: Tree) -> None:
        """Print tree using Rich formatting."""
        if not tree.root:
            self.console.print("[red]Empty tree")
            return

        rich_tree = RichTree(
            self._format_node(tree.root, is_root=True),
            guide_style=self.config.guide_style,
        )
        self._add_children(tree.root, rich_tree)
        self.console.print(rich_tree)

    def _format_node(self, node: Leaf, is_root: bool = False) -> str:
        """Format node information."""
        style = None
        if (
            hasattr(node, "selected")
            and node.selected
            or (
                hasattr(node, "position")
                and hasattr(node.position, "selected")
                and node.position.selected
            )
        ):
            style = self.config.selected_style
        if style is None:
            style = (
                self.config.root_style
                if is_root
                else self.config.leaf_style
                if not node.children
                else self.config.node_style
            )

        parts = []

        if self.config.show_position:
            parts.append(f"[{node.start}-{node.end}]")

        if self.config.show_size:
            parts.append(f"size={node.size}")

        if self.config.show_info and node.info:
            if isinstance(node.info, dict):
                info_str = "Info(" + ", ".join(f"{k}={repr(v)}" for k, v in node.info.items()) + ")"
            else:
                info_str = str(node.info)
            if len(info_str) > 50:  # Truncate if too long
                parts.append("info=...")
            else:
                parts.append(f"info={info_str}")

        return style.render(" ".join(parts))

    def _add_children(self, node: Leaf, rich_node: RichTree) -> None:
        """Recursively add children to Rich tree."""
        for child in node.children:
            child_node = rich_node.add(
                self._format_node(child),
                guide_style=self.config.guide_style,
            )
            self._add_children(child, child_node)
