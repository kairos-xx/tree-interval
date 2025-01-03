"""Rich-based Tree Visualization Implementation."""

from typing import Optional

from rich.console import Console
from rich.style import Style
from rich.tree import Tree as RichTree

from tree_interval.core.interval_core import Leaf, Tree
from tree_interval.rich_printer.config import RichPrintConfig


class RichTreePrinter:
    """Prints tree structures using Rich library."""

    def __init__(
        self,
        config: Optional[RichPrintConfig] = None,
        console: Optional[Console] = None,
    ):
        self.config = config or RichPrintConfig()
        self.console = console or Console()

    def print_tree(self, tree: Tree, root: Optional[Leaf] = None) -> None:
        """Print tree using Rich formatting."""
        root_node = root if root is not None else tree.root
        if not root_node:
            self.console.print("[red]Empty tree")
            return

        rich_tree = RichTree(
            self._format_node(root_node, is_root=True, level=0),
            guide_style=self.config.guide_style,
        )
        self._add_children(root_node, rich_tree, 1)
        self.console.print(rich_tree)

    def _get_node_style(self, node: Leaf, is_root: bool = False) -> Style:
        """Get the style for a node."""
        style = (self.config.root_style if is_root else
                 (self.config.leaf_style
                  if not node.children else self.config.node_style))
        return style or self.config.node_style

    def _format_node(self,
                     node: Leaf,
                     is_root: bool = False,
                     level: int = 0) -> str:
        """Format a node for Rich tree display."""
        style = self._get_node_style(node, is_root)
        parts = []

        if self.config.show_position:
            parts.append(f"[{node.start}-{node.end}]")

        if self.config.show_size:
            parts.append(f"size={node.size}")

        if self.config.show_info and node.info:
            terminal_width = self.config.terminal_size
            current_width = (sum(len(p) for p in parts) + len(parts) * 1) + (
                (level + 1) * 4)

            if isinstance(node.info, dict):
                info_str = ("Info(" +
                            ", ".join(f"{k}={repr(v)}"
                                      for k, v in node.info.items()) + ")")
            else:
                info_str = str(node.info)

            available_width = terminal_width - current_width

            if len(f"info={info_str}") > available_width:
                parts.append("info=...")
            else:
                parts.append(f"info={info_str}")

        return style.render(" ".join(parts))

    def _add_children(self,
                      node: Leaf,
                      rich_node: RichTree,
                      level: int = 0) -> None:
        """Recursively add children to Rich tree."""
        for child in node.children:
            child_node = rich_node.add(
                self._format_node(child, level=level),
                guide_style=self.config.guide_style,
            )
            self._add_children(child, child_node, level + 1)
