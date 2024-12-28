"""
Configuration for tree visualization.
"""

from dataclasses import dataclass


@dataclass
class VisualizationConfig:
    """Configuration for tree visualization.

    Attributes:
        show_info: Whether to display node information
        show_size: Whether to display node sizes
        show_children_count: Whether to display number of children
        position_format: Format for position display
        ('range', 'position', or 'tuple')
    """

    show_info: bool = True
    show_size: bool = True
    show_children_count: bool = False
    position_format: str = "range"  # 'range', 'position', or 'tuple'
