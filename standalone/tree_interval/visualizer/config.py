
"""Configuration for tree visualization."""

from dataclasses import dataclass
from typing import Optional

from rich.style import Style


@dataclass
class VisualizationConfig:
    """Configuration for tree visualization.

    Attributes:
        show_info: Show node info
        show_size: Show node size
        show_children_count: Show number of children
        position_format: Format for position display
        root_style: Style for root node
        node_style: Style for regular nodes
        leaf_style: Style for leaf nodes
    """

    show_info: bool = True
    show_size: bool = True
    show_children_count: bool = False
    position_format: str = "default"
    root_style: Optional[Style] = None
    node_style: Optional[Style] = None
    leaf_style: Optional[Style] = None
