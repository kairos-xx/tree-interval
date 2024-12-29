"""
Tree Visualization Configuration Module.

This module provides configuration options for customizing the visual representation
of tree structures. It allows control over information display, formatting options,
and visual style preferences.

Key Features:
    - Configurable node information display
    - Multiple position format options
    - Size and children count display options
    - Flexible configuration through dataclass

Technical Details:
    - Uses dataclasses for configuration
    - Supports multiple position formats
    - Configurable display options
    - Default configuration provided
"""

from dataclasses import dataclass


@dataclass
class VisualizationConfig:
    """Configuration class for tree visualization settings.

    This class defines the configuration options that control how tree structures
    are visualized. It provides fine-grained control over what information is 
    displayed and how it is formatted.

    Attributes:
        show_info (bool): Controls whether node information is displayed
            Default: True
            Affects: Node content and metadata visibility
            
        show_size (bool): Controls whether node size information is shown
            Default: True
            Format: "size=X" where X is the node size
            
        show_children_count (bool): Controls display of child node counts
            Default: False
            Format: "children=X" where X is the number of children
            
        position_format (str): Determines how position information is formatted
            Options:
                'range': Simple start-end range (default)
                'position': Detailed position object format
                'tuple': Compact tuple representation
            
    Example Usage:
        config = VisualizationConfig(
            show_info=True,
            show_size=False,
            position_format='tuple'
        )
    """

    show_info: bool = True
    show_size: bool = True
    show_children_count: bool = False
    position_format: str = "range"  # 'range', 'position', or 'tuple'
