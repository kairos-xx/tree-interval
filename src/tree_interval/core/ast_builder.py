"""
AST Tree Builder module.
This module provides functionality to build tree structures from Python
Abstract Syntax Trees.
"""

from ast import AST, get_source_segment, iter_child_nodes, parse, walk
from dis import Positions as disposition
from inspect import getsource
from textwrap import dedent
from types import FrameType
from typing import Optional, Union

from .interval_core import Leaf, Position, Tree


class AstTreeBuilder:
    """
    Builds tree structures from Python Abstract Syntax Trees.
    This class handles the conversion of Python source code or
    frame objects into tree structures with position tracking.
    It manages preprocessing, AST parsing, and tree construction
    with positional information.
    Attributes:
        source (Optional[str]): The source code to analyze
        indent_offset (int): Number of spaces in common indentation
        line_offset (int): Line number offset for frame sources
        frame_firstlineno (int): First line number in frame
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
            source: Either a string containing source code or a
                    frame object from which source code
                    can be extracted
        """
        self.cleaned_value_key = "cleaned_value"
        self.source: Optional[str] = None
        self.indent_offset: int = 0
        self.line_offset: int = 0
        self.frame_firstlineno: int = 1
        if isinstance(source, str):
            if not source:
                raise ValueError("Source cannot be empty")
            self.source = source
        elif hasattr(source, "f_code"):
            self.frame_firstlineno = source.f_code.co_firstlineno
            self.source = getsource(source)
        if isinstance(self.source, str):
            self.source = dedent(self.source)

    def _get_node_position(self, node: AST) -> Optional[Position]:
        try:
            lineno = getattr(node, "lineno", None)
            if lineno is None:
                return None
            source_lines = (self.source or "").splitlines(True)
            dis_position = disposition(
                lineno=lineno,
                end_lineno=getattr(node, "end_lineno", lineno),
                col_offset=getattr(node, "col_offset", 0),
                end_col_offset=getattr(node, "end_col_offset",
                                       len(source_lines[-1])),
            )
            start, end = (
                (
                    sum(
                        len(source_lines[i])  # - indent_size
                        for i in range(
                            (getattr(dis_position, "lineno", 1) or 1) - 1)) +
                    (getattr(dis_position, "col_offset", 0) or 0)),
                (
                    sum(
                        len(source_lines[i])  # - indent_size
                        for i in range(
                            (getattr(dis_position, "end_lineno", 1) or 1) - 1))
                    + (getattr(dis_position, "end_col_offset", 0) or 0)),
            )
            position = Position(start, end)
            (
                position.lineno,
                position.end_lineno,
                position.col_offset,
                position.end_col_offset,
            ) = tuple(dis_position)
            return position
        except (IndexError, AttributeError):
            pass
        return None

    def build(self) -> Optional[Tree]:
        if self.source is None:
            raise ValueError("No source code available")
        if not self.source.strip():
            return Tree("")
        tree = parse(self.source)

        return self._build_tree_from_ast(tree)

    def _get_node_value(self, node: AST) -> str:
        """
        Extracts a meaningful value from various AST node types.
        Args:
            node (ast.AST): The AST node to inspect.
        Returns:
            str: The extracted value based on the node type.
        Raises:
            ValueError: If the node type is unsupported.
        """
        import ast
        from sys import version_info

        if isinstance(node, ast.Attribute):
            return node.attr
        elif isinstance(node, ast.Call):
            return self._get_node_value(node.func)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Subscript):
            return self._get_node_value(node.value)
        elif isinstance(node, ast.BinOp):
            return type(node.op).__name__
        elif version_info < (3, 8) and isinstance(node, ast.Num):
            return str(node.n)
        elif version_info < (3, 8) and isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Lambda):
            return "lambda"
        else:
            return ""

    def _build_tree_from_ast(self, ast_tree: AST) -> Optional[Tree]:
        """Build a hierarchical tree structure from an AST.
        This method transforms a Python AST into a position-aware
        tree structure
        where each node maintains:
        1. Source code position information
        2. Parent-child relationships
        3. Type and metadata from AST
        4. Original source snippets
        Args:
            ast_tree: The Python AST to process
        Returns:
            Optional[Tree]: The built tree structure or None if failed
        Raises:
            ValueError: If no source code is available
        """
        if not self.source:
            raise ValueError("No source code available")
        result_tree = Tree[str](self.source)
        root_pos = Position(0, len(self.source))
        result_tree.root = Leaf(
            root_pos,
            info={
                "type": "Module",
                "name": "Module",
                "source": self.source
            },
        )
        root = next(iter(getattr(ast_tree, "body", [None])), None)
        if root is not None:
            root.__dict__["source"] = dedent(self.source)

        nodes_with_positions = []
        for node in walk(ast_tree):

            for v in iter_child_nodes(node):
                v.__dict__.update({
                    "parent":
                    node,
                    "root":
                    next(iter(getattr(ast_tree, "body", [None])), None)
                })
            if position := self._get_node_position(node):
                leaf = Leaf(
                    position,
                    info={
                        "type": node.__class__.__name__,
                        "name": getattr(node, "name", node.__class__.__name__),
                        "source": get_source_segment(dedent(self.source),
                                                     node),
                    },
                )
                setattr(node, self.cleaned_value_key,
                        self._get_node_value(node))
                leaf.ast_node = node
                nodes_with_positions.append(
                    (position.start, position.end, leaf))
        # Sort nodes by position and size to ensure proper nesting
        nodes_with_positions.sort(key=lambda x: (x[0], -(x[1] - x[0])))
        processed = set()
        # Add nodes to tree maintaining proper hierarchy
        for _, _, leaf in nodes_with_positions:
            if not result_tree.root:
                result_tree.root = leaf
                processed.add(leaf)
                continue
            if leaf in processed:
                continue

            best_match = None
            smallest_size = float("inf")
            for start, end, potential_parent in nodes_with_positions:
                if (potential_parent == leaf
                        or potential_parent in leaf.get_ancestors()):
                    continue
                if start <= leaf.start and end >= leaf.end:
                    size = end - start
                    if size < smallest_size:
                        best_match = potential_parent
                        smallest_size = size
            if best_match:
                best_match.add_child(leaf)
                if best_match not in processed:
                    processed.add(leaf)
                    if not best_match.parent:
                        result_tree.add_leaf(best_match)
                        processed.add(best_match)
            else:
                result_tree.add_leaf(leaf)
                processed.add(leaf)
            if not result_tree.root.children:
                result_tree.root.add_child(leaf)

        return result_tree
