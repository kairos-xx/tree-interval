"""
AST Tree Builder module.

This module provides functionality to build tree structures from Python Abstract Syntax Trees.
It includes utilities for source code analysis and tree construction.
"""

# Standard library imports
import ast
from inspect import getsource
from typing import Optional

# Local imports
from main import Leaf, Tree


class AstTreeBuilder:
    """AST Tree Builder for converting Python code into tree structures.
    
    This class takes a frame object and constructs a tree representation
    of the Python code's abstract syntax tree.
    """

    def __init__(self, frame) -> None:
        self.frame = frame
        self.source = None
        self._get_source()

    def _get_source(self) -> None:
        try:
            self.source = ast.unparse(ast.parse(self.frame.f_code.co_code))
        except:
            # Fallback to frame source if available
            if self.frame.f_code.co_firstlineno:
                import inspect
                self.source = inspect.getsource(self.frame.f_code)

    def build(self) -> Tree[str]:
        """Build a tree structure from the Python source code.
        
        Returns:
            A Tree object representing the AST structure
            
        Raises:
            ValueError: If no source code is available
        """
        if not self.source:
            raise ValueError("No source code available")

        tree = ast.parse(self.source)
        result_tree = Tree[str](self.source)

        # Create root node from the Module
        root = Leaf(0, len(self.source), "Module")
        result_tree.root = root

        for node in ast.walk(tree):
            # Check all required position attributes
            if all(
                    hasattr(node, attr) for attr in
                ['lineno', 'end_lineno', 'col_offset', 'end_col_offset']):
                lineno = getattr(node, 'lineno')
                end_lineno = getattr(node, 'end_lineno')
                col_offset = getattr(node, 'col_offset')
                end_col_offset = getattr(node, 'end_col_offset')

                # Convert line numbers to absolute positions in source
                start = self._line_col_to_pos(lineno, col_offset)
                end = self._line_col_to_pos(end_lineno, end_col_offset)

                if start is not None and end is not None:
                    leaf = Leaf(start, end, node.__class__.__name__)
                    result_tree.add_leaf(leaf)

        return result_tree

    def _line_col_to_pos(self, line: int, col: int) -> Optional[int]:
        """Convert line and column numbers to absolute position in source."""
        if not self.source:
            return None
        try:
            lines = self.source.splitlines(True)  # Keep line endings
            pos = 0
            for i in range(line - 1):
                pos += len(lines[i])
            return pos + col
        except:
            return None
