
"""Core module containing fundamental interval tree data structures and operations.

This module provides the foundational classes and utilities for creating and 
manipulating interval-based tree structures. It includes Position management,
Leaf node operations, and Tree construction capabilities.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from typing import (Any, Callable, Dict, Iterator, List, Optional, Set, Tuple,
                   TypeVar, Union)

# Type variable for generic tree operations
T = TypeVar('T')

@dataclass
class Position:
    """Represents a position in source code with both absolute and line-based coordinates.
    
    Attributes:
        start (int): Starting position in absolute terms
        end (int): Ending position in absolute terms
        lineno (Optional[int]): Starting line number (1-based)
        end_lineno (Optional[int]): Ending line number
        col_offset (Optional[int]): Starting column offset
        end_col_offset (Optional[int]): Ending column offset
        absolute_start (Optional[int]): Absolute starting position
        absolute_end (Optional[int]): Absolute ending position
    """
    
    start: int
    end: int
    lineno: Optional[int] = None
    end_lineno: Optional[int] = None
    col_offset: Optional[int] = None
    end_col_offset: Optional[int] = None
    absolute_start: Optional[int] = None
    absolute_end: Optional[int] = None

    def position_as(self, format_type: str = "tuple") -> Union[str, tuple]:
        """Convert position to specified format.
        
        Args:
            format_type (str): Format type ("tuple" or "position")
            
        Returns:
            Union[str, tuple]: Formatted position representation
        """
        if format_type == "position":
            return f"Position({self.start}, {self.end})"
        return (self.start, self.end)

    def __post_init__(self):
        """Initialize absolute positions if not provided."""
        if self.absolute_start is None:
            self.absolute_start = self.start
        if self.absolute_end is None:
            self.absolute_end = self.end

class Leaf:
    """A node in the interval tree structure.
    
    This class represents a node that can contain information and maintain 
    relationships with other nodes in a tree structure.
    
    Attributes:
        position (Position): Node's position in the source
        info (Any): Additional information about the node
        children (List[Leaf]): List of child nodes
        parent (Optional[Leaf]): Reference to parent node
        selected (bool): Whether node is currently selected
        style (Any): Visual style information
        rich_style (Any): Rich text formatting style
    """
    
    def __init__(self,
                 position: Union[Position, tuple, int, None],
                 info: Any = None,
                 end: Optional[int] = None,
                 style: Optional[Any] = None, 
                 rich_style: Optional[Any] = None):
        """Initialize a new Leaf node.
        
        Args:
            position: Position information
            info: Node information
            end: Optional end position if using int
            style: Visual style
            rich_style: Rich text style
        """
        # Position handling
        if position is None:
            position = Position(0, 0)
            
        if isinstance(position, Position):
            self.position = position
        elif isinstance(position, tuple):
            self.position = Position(position[0], position[1])
        else:
            self.position = Position(position, end if end is not None else position)

        # Node properties
        self.info = info
        self.children: List[Leaf] = []
        self.parent: Optional[Leaf] = None
        self.selected = False
        self.style = style
        self.rich_style = rich_style

    @property
    def start(self) -> int:
        """Get start position."""
        return self.position.start

    @property
    def end(self) -> int:
        """Get end position."""
        return self.position.end

    @property 
    def size(self) -> int:
        """Calculate node size including children."""
        return self.end - self.start

    @property
    def next(self) -> Optional[Leaf]:
        """Get next sibling node."""
        if not self.parent:
            return None
        idx = self.parent.children.index(self)
        if idx < len(self.parent.children) - 1:
            return self.parent.children[idx + 1]
        return None

    @property
    def previous(self) -> Optional[Leaf]:
        """Get previous sibling node."""
        if not self.parent:
            return None
        idx = self.parent.children.index(self)
        if idx > 0:
            return self.parent.children[idx - 1]
        return None

    def add_child(self, child: Leaf) -> None:
        """Add a child node.
        
        Args:
            child: Node to add as child
        """
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: Leaf) -> None:
        """Remove a child node.
        
        Args:
            child: Node to remove
        """
        if child in self.children:
            child.parent = None
            self.children.remove(child)
