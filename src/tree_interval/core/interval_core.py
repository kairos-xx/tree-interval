
"""
Core tree data structures and position handling functionality.

This module provides foundational classes for managing tree structures with
interval-based positioning. It includes three main classes:

- Position: Handles position tracking with line numbers and column offsets
- Leaf: Represents nodes in the tree with position information 
- Tree: Manages the overall tree structure and node relationships

Key Features:
    - Precise position tracking with line/column information
    - Parent-child relationship management  
    - Tree traversal capabilities
    - JSON serialization support
    - Rich visualization
"""

from dataclasses import dataclass
from dis import Positions as disposition
from inspect import getframeinfo, getsource
from json import dumps, loads
from types import FrameType
from typing import Any, Dict, Generic, List, NamedTuple, Optional, TypeVar, Union

from .ast_types import AST_TYPES


class LeafStyle(NamedTuple):
    """Style configuration for leaf nodes."""
    color: str
    bold: bool = False


@dataclass 
class PartStatement:
    """Represents a statement part with before and after text"""
    before: str
    after: str


@dataclass
class Statement:
    """Represents a complete statement breakdown"""
    top: PartStatement
    before: str
    self: str
    after: str
    top_marker: str = "^"
    chain_marker: str = "~"
    current_marker: str = "*"

    def as_text(self, top_marker=None, chain_marker=None, current_marker=None) -> str:
        """Generate a text representation of the statement with markers."""
        tm = top_marker or self.top_marker
        cm = chain_marker or self.chain_marker 
        cum = current_marker or self.current_marker

        # Build the full text with markers line by line
        result = []
        
        # Process each part of the statement
        parts = [
            (self.top.before, tm),
            (self.before, cm),
            (self.self, cum),
            (self.after, cm),
            (self.top.after, tm)
        ]
        
        current_line = ""
        current_markers = ""
        
        for text, marker in parts:
            if not text:
                continue
                
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if i > 0:
                    # Add previous line and its markers
                    if current_line:
                        result.append(current_line)
                        result.append(current_markers)
                    current_line = ""
                    current_markers = ""
                    
                current_line += line
                current_markers += ''.join(marker if not c.isspace() else ' ' for c in line)
        
        # Add the last line and its markers
        if current_line:
            result.append(current_line)
            result.append(current_markers)
            
        return '\n'.join(result)

    @property
    def text(self) -> str:
        """Property access for default markers."""
        return self.as_text()

# [Rest of the interval_core.py file remains unchanged...]
