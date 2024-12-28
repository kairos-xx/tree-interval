
"""
AST Tree Builder module.

This module provides functionality to build tree structures from Python
Abstract Syntax Trees.
"""

from ast import AST, parse, unparse, walk
from inspect import getsource
from types import FrameType
from typing import Optional, Union, Tuple

from .interval_core import Leaf, Position, Tree

class AstTreeBuilder:
    def __init__(self, source: Union[FrameType, str]) -> None:
        self.source = None
        if isinstance(source, str):
            self.source = source
        else:
            self.frame = source
            self._get_source()
            
    def _get_source(self) -> None:
        try:
            if self.frame.f_code.co_firstlineno:
                source = getsource(self.frame.f_code)
                lines = source.splitlines()
                # Find common indentation
                common_indent = min(len(line) - len(line.lstrip()) 
                                 for line in lines if line.strip())
                # Remove common indentation and join lines
                self.source = '\n'.join(
                    line[common_indent:] if line.strip() else line 
                    for line in lines)
                self.indent_offset = common_indent
                self.line_offset = self.frame.f_code.co_firstlineno - 1
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

    def _get_node_position(self, node: AST, line_positions: list[Tuple[int, int]]) -> Optional[Position]:
        try:
            lineno = getattr(node, "lineno", None)
            if lineno is None:
                return None
            
            # Adjust line numbers for frame context
            if hasattr(self, 'line_offset'):
                print(self.line_offset)
                start_line = lineno - 1 #+ self.line_offset
                end_lineno = getattr(node, "end_lineno", lineno)
                end_line = end_lineno - 1 #+ self.line_offset
            else:
                start_line = lineno - 1
                end_lineno = getattr(node, "end_lineno", lineno)
                end_line = end_lineno - 1
                
            # Adjust column offsets for dedentation
            col_offset = getattr(node, "col_offset", 0)
            if hasattr(self, 'indent_offset'):
                col_offset = max(0, col_offset - self.indent_offset)

            end_col_offset = getattr(node, "end_col_offset", 0)
            if hasattr(self, 'indent_offset'):
                end_col_offset = max(0, end_col_offset - self.indent_offset)

            if 0 <= start_line < len(line_positions):
                start_pos = line_positions[start_line][0]+self.line_offset
                end_pos = line_positions[end_line][1]+self.line_offset
                position = Position(start_pos, end_pos, node.__class__.__name__)
                position.lineno = lineno+self.line_offset
                position.end_lineno = end_lineno+self.line_offset
                position.col_offset = col_offset
                position.end_col_offset =end_col_offset
                print(position.position_as("position"))
                return position
        except (IndexError, AttributeError):
            pass
        return None

    def build(self) -> Tree[str]:
        if not self.source:
            raise ValueError("No source code available")
        tree = parse(self.source)
        return self._build_tree_from_ast(tree)

    

    def build_from_frame(self) -> Optional[Tree]:
        if not self.source:
            return None
        ast_tree = parse(self.source)
        return self._build_tree_from_ast(ast_tree)

    def _build_tree_from_ast(self, ast_tree: AST) -> Tree[str]:
        result_tree = Tree[str](self.source)
        root_pos = Position(0, len(self.source), "Module")
        result_tree.root = Leaf(root_pos)

        line_positions = self._calculate_line_positions()
        nodes_with_positions = []
        
        for node in walk(ast_tree):
            
            position = self._get_node_position(node, line_positions)
            if position:
                leaf = Leaf(position)
                leaf.ast_node = node
                nodes_with_positions.append((node, leaf))

        for _, leaf in nodes_with_positions:
            result_tree.add_leaf(leaf)

        return result_tree
