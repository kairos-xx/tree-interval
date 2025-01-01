"""
Tree Visualization Configuration Module.

This module defines the configuration options for tree visualization output.
It provides fine-grained control over what information is displayed and how
it is formatted in the visualization output.

Key Features:
    - Toggle display of node information
    - Control size information visibility
    - Configure children count display
    - Multiple position format options
    - Customizable indentation

Technical Details:
    - Uses dataclass for clean configuration
    - Supports multiple position display formats
    - Provides default values for all options
    - Easy to extend with new configuration options
"""

from dataclasses import dataclass


def get_terminal_width() -> int:
    """Get the width of the terminal window."""
    try:
        from shutil import get_terminal_size

        return get_terminal_size().columns
    except Exception:
        return 80  # Default fallback width


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

    terminal_size: int = get_terminal_width()
    show_info: bool = True
    show_size: bool = True
    show_children_count: bool = False
    position_format: str = "range"  # 'range', 'position', or 'tuple'
