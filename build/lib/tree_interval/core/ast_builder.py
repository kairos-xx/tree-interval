"""
AST Tree Builder module.

This module provides functionality to build tree structures from Python
Abstract Syntax Trees.
"""

from ast import AST, parse, unparse, walk
from inspect import getsource
from types import FrameType
from typing import Optional, Union

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
            self.source = unparse(parse(self.frame.f_code.co_code))
        except (SyntaxError, TypeError, ValueError):
            if self.frame.f_code.co_firstlineno:
                self.source = getsource(self.frame.f_code)

    def build(self) -> Tree[str]:
        if not self.source:
            raise ValueError("No source code available")

        tree = parse(self.source)
        if not tree:
            raise ValueError("Failed to parse source code")

        result_tree = Tree[str](self.source)
        if not result_tree:
            raise ValueError("Failed to create result tree")

        root = Leaf(0, len(self.source), "Module")
        result_tree.root = root
        if not result_tree.root:
            raise ValueError("Failed to set root node")

        for node in walk(tree):
            lineno = getattr(node, "lineno", None)
            end_lineno = getattr(node, "end_lineno", None)
            col_offset = getattr(node, "col_offset", None)
            end_col_offset = getattr(node, "end_col_offset", None)

            if all(
                x is not None for x in [lineno, col_offset, end_lineno, end_col_offset]
            ):
                if (
                    isinstance(lineno, int)
                    and isinstance(col_offset, int)
                    and isinstance(end_lineno, int)
                    and isinstance(end_col_offset, int)
                ):
                    start = self._line_col_to_pos(lineno, col_offset)
                    end = self._line_col_to_pos(end_lineno, end_col_offset)

                    # Collect all fields and their values
                    fields_info = {}
                    for field in node._fields:
                        value = getattr(node, field, None)
                        if isinstance(value, (str, int, float, bool)):
                            fields_info[field] = value
                        elif isinstance(value, AST):
                            fields_info[field] = {
                                "type": value.__class__.__name__,
                                "fields": {
                                    k: getattr(value, k, None) for k in value._fields
                                },
                            }
                        elif isinstance(value, list):
                            fields_info[field] = [
                                {
                                    "type": item.__class__.__name__,
                                    "fields": {
                                        k: getattr(item, k, None) for k in item._fields
                                    },
                                }
                                if isinstance(item, AST)
                                else item
                                for item in value
                            ]

                    node_info = {
                        "type": node.__class__.__name__,
                        "fields": fields_info,
                        "_fields": node._fields,
                    }

                    leaf = Leaf(
                        Position(start if start is not None else 0, end, node_info),
                        None,
                    )
                    leaf.position._col_offset = col_offset
                    leaf.position._end_col_offset = end_col_offset
                    result_tree.add_leaf(leaf)
                continue

            elif all(x is not None for x in [lineno, col_offset]):
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
                    # Collect all fields and their values
                    fields_info = {}
                    for field in node._fields:
                        value = getattr(node, field, None)
                        if isinstance(value, (str, int, float, bool)):
                            fields_info[field] = value
                        elif isinstance(value, AST):
                            fields_info[field] = {
                                "type": value.__class__.__name__,
                                "fields": {
                                    k: getattr(value, k, None) for k in value._fields
                                },
                            }
                        elif isinstance(value, list):
                            fields_info[field] = [
                                {
                                    "type": item.__class__.__name__,
                                    "fields": {
                                        k: getattr(item, k, None) for k in item._fields
                                    },
                                }
                                if isinstance(item, AST)
                                else item
                                for item in value
                            ]

                    node_info = {
                        "type": node.__class__.__name__,
                        "fields": fields_info,
                        "_fields": node._fields,
                    }

                    leaf = Leaf(
                        Position(start if start is not None else 0, end, node_info),
                        None,
                    )
                    leaf.position._col_offset = col_offset
                    leaf.position._end_col_offset = (
                        end_col_offset
                        if end_col_offset is not None
                        else (col_offset + 1 if col_offset is not None else 1)
                    )
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
