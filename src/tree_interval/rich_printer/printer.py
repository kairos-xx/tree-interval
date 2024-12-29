
"""Rich-based tree printer implementation.

This module provides functionality for pretty-printing tree structures using
the Rich library, with support for custom styling and formatting options.
"""

from typing import Optional

from rich.console import Console
from rich.style import Style
from rich.tree import Tree as RichTree

from ..core.interval_core import Leaf, Tree
from .config import RichPrintConfig

class RichTreePrinter:
    """Prints tree structures using Rich library with advanced formatting.
    
    This class handles the visualization of tree structures with customizable
    styles, colors, and formatting options using the Rich library.
    
    Attributes:
        config (RichPrintConfig): Configuration for printing
        console (Console): Rich console instance
    """

    def __init__(self,
                 config: Optional[RichPrintConfig] = None,
                 console: Optional[Console] = None):
        """Initialize printer with configuration.
        
        Args:
            config: Custom print configuration
            console: Custom Rich console
        """
        self.config = config or RichPrintConfig()
        self.console = console or Console()

    def print_tree(self, tree: Tree) -> None:
        """Print tree using Rich formatting.
        
        Args:
            tree: Tree structure to print
        """
        # Handle empty tree case
        if not tree.root:
            self.console.print("[red]Empty tree")
            return

        # Create root node with formatting
        rich_tree = RichTree(
            self._format_node(tree.root, is_root=True),
            guide_style=self.config.guide_style
        )
        
        # Recursively add all children
        self._add_children(tree.root, rich_tree)
        self.console.print(rich_tree)

    def _format_node(self, node: Leaf, is_root: bool = False) -> str:
        """Format node information with appropriate styling.
        
        Args:
            node: Node to format
            is_root: Whether node is root
            
        Returns:
            str: Formatted node string
        """
        # Style priority: rich_style > selected > type-based > default
        style = None

        # Determine appropriate style
        if hasattr(node, 'rich_style') and node.rich_style:
            style = node.rich_style
        elif hasattr(node, "selected") and node.selected:
            style = self.config.selected_style
        elif isinstance(node.info, dict) and "type" in node.info:
            # Apply type-specific styling
            if node.info["type"] == "Module":
                style = Style(color="green", bold=True)
            elif node.info["type"] == "FunctionDef":
                style = Style(color="blue", bold=False)
            else:
                style = Style(color="grey70", bold=False)
        else:
            style = (self.config.root_style if is_root else
                    (self.config.leaf_style if not node.children 
                     else self.config.node_style))

        # Ensure style exists
        if not style:
            style = self.config.node_style

        # Build display components
        parts = []
        if isinstance(node.info, dict):
            # Format AST nodes
            node_type = node.info.get('type', '')
            node_name = node.info.get('name', '')
            if node_name:
                parts.append(f"{node_type}({node_name})")
            else:
                parts.append(node_type)
        else:
            # Format regular nodes
            parts.append(str(node.info))

        # Add position information if configured
        if self.config.show_position:
            parts.append(f"[{node.start}-{node.end}]")

        # Add size information if configured
        if self.config.show_size:
            parts.append(f"size={node.size}")

        # Add node info if configured
        if self.config.show_info and node.info:
            # Get terminal width for formatting
            terminal_width = self._get_terminal_width()
            current_width = sum(len(p) for p in parts) + len(parts) * 1

            # Format node info
            if isinstance(node.info, dict):
                info_str = ("Info(" +
                           ", ".join(f"{k}={repr(v)}"
                                   for k, v in node.info.items()) + ")")
            else:
                info_str = str(node.info)

            # Truncate if too long
            available_width = terminal_width - current_width - 10
            if len(info_str) > available_width:
                parts.append("info=...")
            else:
                parts.append(f"info={info_str}")

        return style.render(" ".join(parts))

    def _add_children(self, node: Leaf, rich_node: RichTree) -> None:
        """Recursively add children to Rich tree.
        
        Args:
            node: Parent node
            rich_node: Rich tree node
        """
        for child in node.children:
            child_node = rich_node.add(
                self._format_node(child),
                guide_style=self.config.guide_style,
            )
            self._add_children(child, child_node)

    @staticmethod
    def _get_terminal_width() -> int:
        """Get terminal width safely.
        
        Returns:
            int: Terminal width or default 80
        """
        try:
            import shutil
            columns, _ = shutil.get_terminal_size()
            return columns
        except (OSError, ValueError):
            return 80
