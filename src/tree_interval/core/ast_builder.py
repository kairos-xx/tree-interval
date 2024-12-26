
"""
AST Tree Builder module.

This module provides functionality to build tree structures from Python
Abstract Syntax Trees.
"""

import ast
from inspect import getsource
from typing import Optional

from ..core.interval_core import Tree, Leaf


class AstTreeBuilder:
    def __init__(self, frame) -> None:
        self.frame = frame
        self.source = None
        self._get_source()

    def _get_source(self) -> None:
        try:
            self.source = ast.unparse(ast.parse(self.frame.f_code.co_code))
        except (SyntaxError, TypeError, ValueError):
            if self.frame.f_code.co_firstlineno:
                self.source = getsource(self.frame.f_code)

    def build(self) -> Tree[str]:
        if not self.source:
            raise ValueError("No source code available")

        tree = ast.parse(self.source)
        result_tree = Tree[str](self.source)
        root = Leaf(0, len(self.source), "Module")
        result_tree.root = root

        for node in ast.walk(tree):
            lineno = getattr(node, 'lineno', None)
            end_lineno = getattr(node, 'end_lineno', None)
            col_offset = getattr(node, 'col_offset', None)
            end_col_offset = getattr(node, 'end_col_offset', None)
            
            if all(x is not None for x in [lineno, col_offset]):
                if isinstance(lineno, int) and isinstance(col_offset, int):
                    start = self._line_col_to_pos(lineno, col_offset)
                    if isinstance(end_lineno, int) and isinstance(end_col_offset, int):
                        end = self._line_col_to_pos(end_lineno, end_col_offset)
                    else:
                        end = None
                else:
                    start = None
                    end = None

                if start is not None and end is not None:
                    leaf = Leaf(start, end, node.__class__.__name__)
                    result_tree.add_leaf(leaf)

        return result_tree

    def _line_col_to_pos(self, line: int, col: int) -> Optional[int]:
        if not self.source:
            return None
        try:
            lines = self.source.splitlines(True)
            pos = 0
            for i in range(line - 1):
                pos += len(lines[i])
            return pos + col
        except Exception:
            return None