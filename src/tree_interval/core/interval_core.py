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

from ..visualizer import TreeVisualizer, VisualizationConfig

# Type variable for generic tree operations
T = TypeVar('T')

class Tree:
    """A tree structure that manages interval-based nodes.
    
    Attributes:
        source (str): Source identifier for the tree
        root (Optional[Leaf]): Root node of the tree
        start_lineno (int): Starting line number
        indent_size (int): Indentation size for visualization
    """
    
    def __init__(self, source: str = "", start_lineno: int = 1, indent_size: int = 4):
        self.source = source
        self.root: Optional[Leaf] = None
        self.start_lineno = start_lineno
        self.indent_size = indent_size

    def add_leaf(self, leaf: Leaf) -> None:
        """Add a leaf to the tree under the root."""
        if self.root:
            self.root.add_child(leaf)
            
    def find_best_match(self, start: int, end: int) -> Optional[Leaf]:
        """Find the best matching node for given interval."""
        if not self.root:
            return None
        return self._find_best_match(self.root, start, end)
        
    def _find_best_match(self, node: Leaf, start: int, end: int) -> Optional[Leaf]:
        """Recursively find best matching node."""
        best_match = None
        if node.start <= start and node.end >= end:
            best_match = node
            for child in node.children:
                child_match = self._find_best_match(child, start, end)
                if child_match:
                    best_match = child_match
        return best_match

    def flatten(self) -> List[Leaf]:
        """Return flattened list of all nodes."""
        if not self.root:
            return []
        return self._flatten_helper(self.root, [])
        
    def _flatten_helper(self, node: Leaf, result: List[Leaf]) -> List[Leaf]:
        """Helper for flatten operation."""
        result.append(node)
        for child in node.children:
            self._flatten_helper(child, result)
        return result

    def to_json(self) -> str:
        """Convert tree to JSON string."""
        if not self.root:
            return "{}"
        return json.dumps(self._node_to_dict(self.root))
        
    @staticmethod
    def from_json(json_str: str) -> 'Tree':
        """Create tree from JSON string."""
        tree = Tree()
        if json_str != "{}":
            data = json.loads(json_str)
            tree.root = Tree._dict_to_node(data)
        return tree

    def _node_to_dict(self, node: Leaf) -> Dict:
        """Convert node to dictionary."""
        return {
            "start": node.start,
            "end": node.end,
            "info": node.info,
            "children": [self._node_to_dict(child) for child in node.children]
        }

    @staticmethod
    def _dict_to_node(data: Dict) -> Leaf:
        """Create node from dictionary."""
        node = Leaf(Position(data["start"], data["end"]), data["info"])
        for child_data in data["children"]:
            child = Tree._dict_to_node(child_data)
            node.add_child(child)
        return node

    def visualize(self, config: Optional[VisualizationConfig] = None) -> None:
        """Visualize the tree structure using TreeVisualizer."""
        TreeVisualizer.visualize(self, config)

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
    def lineno(self) -> Optional[int]:
        """Get line number."""
        return self.position.lineno if hasattr(self.position, 'lineno') else None

    @property
    def end_lineno(self) -> Optional[int]:
        """Get end line number."""
        return self.position.end_lineno if hasattr(self.position, 'end_lineno') else None

    @property
    def col_offset(self) -> Optional[int]:
        """Get column offset."""
        return self.position.col_offset if hasattr(self.position, 'col_offset') else None

    @property
    def end_col_offset(self) -> Optional[int]:
        """Get end column offset."""
        return self.position.end_col_offset if hasattr(self.position, 'end_col_offset') else None

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

    def find_sibling(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first sibling that matches the criteria.
        
        Args:
            criteria: Function that takes a Leaf node and returns bool
            
        Returns:
            Matching sibling node or None if not found
        """
        if not self.parent:
            return None
        for child in self.parent.children:
            if child != self and criteria(child):
                return child
        return None

    def find_child(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first child node that matches the given criteria.
        
        Args:
            criteria: Function that takes a Leaf node and returns bool
            
        Returns:
            Matching child node or None if not found
        """
        for child in self.children:
            if criteria(child):
                return child
            result = child.find_child(criteria)
            if result:
                return result
        return None

    def find_parent(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first parent that matches the criteria.
        
        Args:
            criteria: Function that takes a Leaf node and returns bool
            
        Returns:
            Matching parent node or None if not found
        """
        current = self.parent
        while current:
            if criteria(current):
                return current
            current = current.parent
        return None

    def find_common_ancestor(self, other: "Leaf") -> Optional["Leaf"]:
        """Find the common ancestor between this node and another node.
        
        Args:
            other: Another Leaf node to find common ancestor with
            
        Returns:
            Common ancestor node or None if not found
        """
        if not other:
            return None
            
        # Get path to root for current node
        current_path = set()
        current = self
        while current:
            current_path.add(current)
            current = current.parent
            
        # Check other's ancestors against current path
        current = other
        while current:
            if current in current_path:
                return current
            current = current.parent
            
        return None

    def find_first_multi_child_ancestor(self) -> Optional["Leaf"]:
        """Find the first ancestor that has multiple children.
        
        Returns:
            First ancestor with multiple children or None if not found
        """
        current = self.parent
        while current:
            if len(current.children) > 1:
                return current
            current = current.parent
        return None