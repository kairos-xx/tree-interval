
"""AST Tree Builder implementation."""
import ast
from ast import AST, NodeVisitor
from inspect import FrameType
from textwrap import dedent
from typing import Any, Optional

from tree_interval.core.interval_core import (
    Leaf,
    Position,
    Statement,
    Tree,
)
from tree_interval.core.ast_types import AST_TYPES


class AstTreeBuilder(NodeVisitor):
    """AST Tree Builder class for converting Python code into tree structures."""

    def __init__(
        self,
        source: Optional[str] = None,
        indent_offset: int = 0,
        line_offset: int = 0,
        frame_firstlineno: Optional[int] = None,
    ) -> None:
        self.source = source
        self.indent_offset = indent_offset
        self.line_offset = line_offset
        self.frame_firstlineno = frame_firstlineno
        self.tree = Tree("AST")
        self.current_node: Optional[Leaf] = None

    def build(self) -> Optional[Tree]:
        """Build tree from source code."""
        if not self.source:
            return None

        try:
            tree = ast.parse(dedent(self.source))
            self.visit(tree)
            return self.tree
        except SyntaxError:
            return None

    def create_node(self, node: AST) -> Optional[Leaf]:
        """Create a tree node from AST node."""
        pos = Position(0, 0)

        if hasattr(node, "lineno"):
            lineno = node.lineno + (
                self.line_offset if self.frame_firstlineno is None else 0
            )
            end_lineno = (
                getattr(node, "end_lineno", lineno)
                + (self.line_offset if self.frame_firstlineno is None else 0)
            )
            pos.lineno = lineno
            pos.end_lineno = end_lineno

        if hasattr(node, "col_offset"):
            pos.col_offset = node.col_offset + self.indent_offset
            pos.end_col_offset = getattr(
                node, "end_col_offset", pos.col_offset
            )

        node_type = node.__class__.__name__
        info = {"type": node_type}

        if hasattr(node, "name"):
            info["name"] = node.name
        elif hasattr(node, "id"):
            info["name"] = node.id

        leaf = Leaf(pos, info=info)
        leaf.ast_node = node
        return leaf

    def generic_visit(self, node: AST) -> Any:
        """Visit AST node and create corresponding tree node."""
        new_node = self.create_node(node)
        if new_node:
            if not self.tree.root:
                self.tree.root = new_node
            elif self.current_node:
                self.current_node.add_child(new_node)

            previous_node = self.current_node
            self.current_node = new_node
            super().generic_visit(node)
            self.current_node = previous_node
            
            # Add statement information
            if node.__class__.__name__ in AST_TYPES:
                new_node.info["is_statement"] = AST_TYPES[node.__class__.__name__]["statement"]
