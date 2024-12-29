"""Rich-based tree printer implementation."""
from typing import Optional

from rich.console import Console
from rich.style import Style
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
            guide_style=self.config.guide_style
        )
        self._add_children(tree.root, rich_tree)
        self.console.print(rich_tree)

    def _format_node(self, node: Leaf, is_root: bool = False) -> str:
        """Format node information."""
        # Determine style priority: rich_style > selected > type-based > default
        style = None

        # Check for custom rich_style or selected state
        if hasattr(node, 'rich_style') and node.rich_style:
            style = node.rich_style
        elif hasattr(node, "selected") and node.selected:
            style = self.config.selected_style
        # Check for type-based styling
        elif isinstance(node.info, dict) and "type" in node.info:
            if node.info["type"] == "Module":
                style = Style(color="green", bold=True)
            elif node.info["type"] == "FunctionDef":
                style = Style(color="blue", bold=False)
            else:
                style = Style(color="grey70", bold=False)
        else:
            style = (self.config.root_style if is_root else
                     (self.config.leaf_style
                      if not node.children else self.config.node_style))

        # Ensure style is applied
        if not style:
            style = self.config.node_style

        # Build display string
        parts = []
        if isinstance(node.info, dict):
            # For AST nodes, show type and name if available
            node_type = node.info.get('type', '')
            node_name = node.info.get('name', '')
            if node_name:
                parts.append(f"{node_type}({node_name})")
            else:
                parts.append(node_type)
        else:
            # For other nodes, show info directly
            parts.append(str(node.info))

        if self.config.show_position:
            parts.append(f"[{node.start}-{node.end}]")

        if self.config.show_size:
            parts.append(f"size={node.size}")

        def get_terminal_width() -> int:
            try:
                import shutil

                columns, _ = shutil.get_terminal_size()
                return columns
            except (OSError, ValueError):
                return 80

        if self.config.show_info and node.info:
            terminal_width = get_terminal_width()
            current_width = (sum(len(p) for p in parts) + len(parts) * 1
                             )  # Add spaces between parts

            if isinstance(node.info, dict):
                info_str = ("Info(" +
                            ", ".join(f"{k}={repr(v)}"
                                      for k, v in node.info.items()) + ")")
            else:
                info_str = str(node.info)

            available_width = (terminal_width - current_width - 10
                               )  # Extra padding for rich formatting

            if len(info_str) > available_width:
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