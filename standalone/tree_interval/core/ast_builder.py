
"""AST Tree Builder Module.

This module is responsible for building tree structures from Python AST nodes.
"""

import ast
from typing import Any, Dict, List, Optional, Set, Tuple, Type, cast

from tree_interval import Tree
from tree_interval.core.ast_types import TYPES_MAP
from tree_interval.core.interval_core import Leaf, Position


def _node_to_dict(node: Any) -> Dict[str, Any]:
    """Convert AST node to dictionary representation.

    Args:
        node: AST node to convert

    Returns:
        Dict containing node info
    """
    result: Dict[str, Any] = {}
    for key, value in ast.iter_fields(node):
        if isinstance(value, ast.AST):
            result[key] = _node_to_dict(value)
        elif isinstance(value, list):
            result[key] = [
                _node_to_dict(x) if isinstance(x, ast.AST) else x
                for x in value
            ]
        else:
            result[key] = value
    return result


class AstTreeBuilder:
    """Builder for creating trees from Python AST nodes."""

    def __init__(
        self,
        source: str,
        start_lineno: int = 1,
        indent_size: int = 4,
    ) -> None:
        """Initialize AST tree builder.

        Args:
            source: Python source code
            start_lineno: Starting line number for tree 
            indent_size: Number of spaces per indent level
        """
        self.source = source
        self.tree = Tree(source, start_lineno, indent_size)
        self.lines = source.splitlines()

    def _get_node_source(self, node: ast.AST) -> str:
        """Get source code for given AST node.

        Args:
            node: AST node

        Returns:
            Source code string
        """
        if not hasattr(node, "lineno") or not hasattr(node, "col_offset"):
            return ""

        start_line = node.lineno - 1  # type: ignore
        end_line = (
            node.end_lineno - 1  # type: ignore
            if hasattr(node, "end_lineno")
            else start_line
        )

        if start_line >= len(self.lines) or end_line >= len(self.lines):
            return ""

        if start_line == end_line:
            line = self.lines[start_line]
            start_col = node.col_offset  # type: ignore
            end_col = (
                node.end_col_offset  # type: ignore
                if hasattr(node, "end_col_offset")
                else len(line)
            )
            return line[start_col:end_col]

        result = []
        for i in range(start_line, end_line + 1):
            if i == start_line:
                result.append(self.lines[i][node.col_offset :])  # type: ignore
            elif i == end_line:
                result.append(
                    self.lines[i][: node.end_col_offset]  # type: ignore
                    if hasattr(node, "end_col_offset")
                    else self.lines[i]
                )
            else:
                result.append(self.lines[i])
        return "\n".join(result)

    def _create_leaf(self, node: ast.AST) -> Optional[Leaf]:
        """Create a Leaf node from AST node.

        Args:
            node: AST node

        Returns:
            Leaf node or None if node has no position info
        """
        if not hasattr(node, "lineno") or not hasattr(node, "col_offset"):
            return None

        start_pos = (
            sum(len(line) + 1 for line in self.lines[: node.lineno - 1])  # type: ignore
            + node.col_offset  # type: ignore
        )
        pos = Position(start_pos, start_pos)
        pos.lineno = node.lineno  # type: ignore
        pos.col_offset = node.col_offset  # type: ignore

        if hasattr(node, "end_lineno"):
            pos.end_lineno = node.end_lineno  # type: ignore
        if hasattr(node, "end_col_offset"):
            pos.end_col_offset = node.end_col_offset  # type: ignore

        source = self._get_node_source(node)
        pos.end = pos.start + len(source)

        node_type = type(node)
        type_name = node_type.__name__
        info = {
            "type": type_name,
            "source": source,
            "attributes": _node_to_dict(node),
        }

        if type_name in TYPES_MAP:
            info.update(TYPES_MAP[type_name](node))

        leaf = Leaf(pos, info)
        leaf.ast_node = node
        return leaf

    def _process_node(
        self, node: ast.AST, parent: Optional[Leaf] = None
    ) -> Optional[Leaf]:
        """Process AST node and create corresponding Leaf node.

        Args:
            node: AST node to process
            parent: Parent Leaf node

        Returns:
            Created Leaf node or None
        """
        leaf = self._create_leaf(node)
        if not leaf:
            return None

        if parent:
            parent.add_child(leaf)
        elif not self.tree.root:
            self.tree.root = leaf

        for child_node in ast.iter_child_nodes(node):
            child_leaf = self._process_node(child_node, leaf)
            if child_leaf:
                leaf.add_child(child_leaf)

        return leaf

    def build(self) -> Optional[Tree]:
        """Build tree from source code.

        Returns:
            Built tree or None if parsing fails
        """
        try:
            root = ast.parse(self.source)
            self._process_node(root)
            return self.tree
        except SyntaxError:
            return None
