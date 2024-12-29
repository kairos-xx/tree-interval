
"""
AST Tree Builder module.

This module provides functionality to build tree structures from Python
Abstract Syntax Trees.
"""

from ast import AST, parse, unparse, walk
from inspect import getsource
from types import FrameType
from typing import Optional, Tuple, Union

from .interval_core import Leaf, Position, Tree


class AstTreeBuilder:
    """
    Builds tree structures from Python Abstract Syntax Trees (AST).
    
    This class handles the conversion of Python source code or frame objects into
    tree structures with precise position tracking. It manages source code 
    preprocessing, AST parsing, and tree construction with positional information.

    Attributes:
        source (Optional[str]): The source code to analyze
        indent_offset (int): Number of spaces in common indentation
        line_offset (int): Line number offset for frame sources
        frame_firstlineno (Optional[int]): First line number in frame

    Technical Details:
        - Handles both string and frame input sources
        - Maintains source code position awareness
        - Processes indentation for accurate positioning
        - Supports AST node position mapping
        - Builds hierarchical tree structures
    """

    def __init__(self, source: Union[FrameType, str]) -> None:
        """
        Initialize the AST builder with source code or a frame.
        
        Args:
            source: Either a string containing source code or a frame object
                   from which source code can be extracted
        """
        self.source: Optional[str] = None
        self.indent_offset: int = 0
        self.line_offset: int = 0
        self.frame_firstlineno: Optional[int] = None

        if isinstance(source, str):
            self.source = source
        else:
            self.frame_firstlineno = source.f_code.co_firstlineno
            self.source = getsource(source)
            self._get_source()

    def _get_source(self) -> None:
        """
        Extract and process source code from the input source.
        
        This method handles:
        - Source code extraction from frames
        - Common indentation detection
        - Line number offset calculation
        - Source code normalization
        
        Implementation Details:
        - Removes common indentation from all lines
        - Preserves empty lines
        - Adjusts line numbers based on frame context
        - Handles potential extraction errors
        """
        try:
            if self.source is None or not isinstance(self.source, str):
                return
            if not self.frame_firstlineno:
                return
            lines = self.source.splitlines()
            if not lines:
                return

            # Find common indentation
            indented_lines = [line for line in lines if line.strip()]
            if not indented_lines:
                return

            common_indent = min(
                len(line) - len(line.lstrip()) for line in indented_lines)

            # Remove common indentation and join lines
            self.source = "\n".join(
                line[common_indent:] if line.strip() else line
                for line in lines)
            self.indent_offset = common_indent
            self.line_offset = self.frame_firstlineno - 1
        except (SyntaxError, TypeError, ValueError):
            pass

    def _calculate_line_positions(self) -> list[Tuple[int, int]]:
        if not self.source:
            return []
        positions = []
        start = 0
        lines = self.source.splitlines(keepends=True)
        for line in lines:
            positions.append((start, start + len(line)))
            start += len(line)
        return positions

    def _get_node_position(
            self, node: AST,
            line_positions: list[Tuple[int, int]]) -> Optional[Position]:
        try:
            lineno = getattr(node, "lineno", None)
            if lineno is None:
                return None

            # Adjust line numbers for frame context
            if hasattr(self, "line_offset"):
                start_line = lineno - 1  # + self.line_offset
                end_lineno = getattr(node, "end_lineno", lineno)
                end_line = end_lineno - 1  # + self.line_offset
            else:
                start_line = lineno - 1
                end_lineno = getattr(node, "end_lineno", lineno)
                end_line = end_lineno - 1

            # Adjust column offsets for dedentation
            col_offset = getattr(node, "col_offset", 0)
            if hasattr(self, "indent_offset"):
                col_offset = max(0, col_offset - self.indent_offset)

            end_col_offset = getattr(node, "end_col_offset", 0)
            if hasattr(self, "indent_offset"):
                end_col_offset = max(0, end_col_offset - self.indent_offset)

            if 0 <= start_line < len(line_positions):
                start_pos = line_positions[start_line][0] + col_offset
                end_pos = line_positions[end_line][0] + end_col_offset
                position = Position(start_pos, end_pos)
                position.lineno = lineno + self.line_offset
                position.end_lineno = end_lineno + self.line_offset
                position.col_offset = col_offset
                position.end_col_offset = end_col_offset
                return position
        except (IndexError, AttributeError):
            pass
        return None

    def build(self) -> Optional[Tree]:
        if not self.source:
            raise ValueError("No source code available")
        tree = parse(self.source)
        return self._build_tree_from_ast(tree)

    def build_from_frame(self) -> Optional[Tree]:
        if not self.source:
            return None
        ast_tree = parse(self.source)
        return self._build_tree_from_ast(ast_tree)

    def _build_tree_from_ast(self, ast_tree: AST) -> Optional[Tree]:
        if not self.source:
            raise ValueError("No source code available")
        result_tree = Tree[str](self.source)
        root_pos = Position(0, len(self.source), "Module")
        result_tree.root = Leaf(root_pos)

        line_positions = self._calculate_line_positions()
        nodes_with_positions = []

        for node in walk(ast_tree):
            position = self._get_node_position(node, line_positions)
            if position:
                leaf = Leaf(
                    position,
                    info={
                        "type": node.__class__.__name__,
                        "name": getattr(node, 'name', node.__class__.__name__),
                        "source": unparse(node)
                    },
                )
                leaf.ast_node = node
                nodes_with_positions.append(
                    (position.start, position.end, leaf))

        # Sort nodes by position and size to ensure proper nesting
        nodes_with_positions.sort(key=lambda x: (x[0], -(x[1] - x[0])))

        # Add nodes to tree maintaining proper hierarchy
        for _, _, leaf in nodes_with_positions:
            if not result_tree.root:
                result_tree.root = leaf
            else:
                # Find the innermost containing node
                best_match = None
                for start, end, potential_parent in nodes_with_positions:
                    if (start <= leaf.start and end >= leaf.end
                            and potential_parent != leaf and
                        (not best_match or
                         (end - start) < (best_match.end - best_match.start))):
                        best_match = potential_parent

                if best_match:
                    best_match.add_child(leaf)
                else:
                    result_tree.add_leaf(leaf)

        return result_tree

    def _line_col_to_pos(self, lineno: int, col_offset: int) -> Optional[int]:
        """Convert line and column to absolute position."""
        if not self.source or not isinstance(self.source, str):
            return None
        lines = self.source.splitlines()
        if not lines:
            return None
        pos = sum(len(line) + 1 for line in lines[:lineno - 1]) + col_offset
        return pos
