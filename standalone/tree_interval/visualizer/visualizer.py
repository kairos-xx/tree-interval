
"""Tree visualization implementation."""

from typing import Optional

from rich.tree import Tree as RichTree
from rich.console import Console

from tree_interval.core.interval_core import Leaf, Tree
from tree_interval.visualizer.config import VisualizationConfig


class TreeVisualizer:
    """Visualizer for tree structures."""

    @staticmethod
    def visualize(tree: Tree, config: Optional[VisualizationConfig] = None, root: Optional[Leaf] = None) -> None:
        """Visualize tree structure.

        Args:
            tree: Tree to visualize
            config: Visualization configuration
            root: Optional root node to start visualization from
        """
        if not config:
            config = VisualizationConfig()

        if not tree.root:
            return

        console = Console()
        rich_tree = RichTree(f"[bold]{tree.source}[/bold]")
        
        start_node = root if root else tree.root
        TreeVisualizer._build_rich_tree(start_node, rich_tree, config)
        
        console.print(rich_tree)

    @staticmethod
    def _build_rich_tree(node: Leaf, rich_tree: RichTree, config: VisualizationConfig) -> None:
        """Build rich tree recursively.

        Args:
            node: Current node
            rich_tree: Rich tree to build
            config: Visualization configuration
        """
        for child in node.children:
            label_parts = []
            
            if config.show_info and hasattr(child, 'info'):
                label_parts.append(str(child.info))
            
            if config.show_size:
                label_parts.append(f"({child.size})")
            
            if config.show_children_count:
                label_parts.append(f"[{len(child.children)}]")
            
            label = " ".join(label_parts)
            
            style = child.rich_style if hasattr(child, 'rich_style') else None
            branch = rich_tree.add(label, style=style)
            
            TreeVisualizer._build_rich_tree(child, branch, config)
