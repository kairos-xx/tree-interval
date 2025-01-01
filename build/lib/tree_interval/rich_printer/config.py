"""
Rich Tree Printer Configuration Module.

This module provides configuration options for the Rich-based
tree visualization.
It defines styles and display preferences for different node types
and components of the tree visualization.

Key Features:
    - Customizable node styling
    - Different styles for root, nodes, and leaves
    - Information display toggles
    - Guide style customization
    - Selected node highlighting

Technical Details:
    - Uses Rich Style objects for formatting
    - Supports ANSI color codes
    - Configurable indentation
    - Toggle-based information display
"""

from dataclasses import dataclass

from rich.style import Style


def get_terminal_width() -> int:
    """Get the width of the terminal window."""
    try:
        from shutil import get_terminal_size

        return get_terminal_size().columns
    except Exception:
        return 80  # Default fallback width


@dataclass
class RichPrintConfig:
    """Configuration for Rich tree visualization."""

    terminal_size: int = get_terminal_width()
    show_info: bool = True
    show_size: bool = True
    show_position: bool = True
    indent_size: int = 2
    root_style: Style = Style(color="green", bold=True)
    node_style: Style = Style(color="blue")
    leaf_style: Style = Style(color="cyan")
    info_style: Style = Style(color="yellow", italic=True)
    guide_style: Style = Style(color="grey70")
    selected_style: Style = Style(color="red", bold=True)
