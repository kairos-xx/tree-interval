
import ast
from typing import Any, Optional, Union

from tree_interval.core.ast_types import NODES
from tree_interval.core.interval_core import Leaf, Position, Tree


class ASTBuilder:
    """Builds a Tree structure from Python AST."""

    @staticmethod
    def from_source(source: str) -> Tree:
        """Build Tree from source code string."""
        tree = ast.parse(source)
        return ASTBuilder.from_ast(tree, source)

    @staticmethod
    def from_ast(tree: ast.AST, source: Optional[str] = None) -> Tree:
        """Build Tree from AST."""
        result = Tree("AST" if source is None else source)
        if source:
            result.source = source
        root = ASTBuilder._build_node(tree)
        if root:
            result.root = root
        return result

    @staticmethod
    def _get_position(node: Union[ast.AST, None]) -> Position:
        """Extract position information from AST node."""
        if not node:
            return Position(0, 0)

        lineno = getattr(node, "lineno", 0)
        end_lineno = getattr(node, "end_lineno", lineno)
        col_offset = getattr(node, "col_offset", 0)
        end_col_offset = getattr(node, "end_col_offset", 0)

        pos = Position(0, 0)
        pos.lineno = lineno
        pos.end_lineno = end_lineno
        pos.col_offset = col_offset
        pos.end_col_offset = end_col_offset
        return pos

    @staticmethod
    def _get_node_info(node: ast.AST) -> dict[str, Any]:
        """Extract relevant information from AST node."""
        info: dict[str, Any] = {"type": node.__class__.__name__}
        
        # Add name if present
        if hasattr(node, "name"):
            info["name"] = node.name
        elif hasattr(node, "id"):
            info["name"] = node.id
        
        # Add value for literals
        if hasattr(node, "value"):
            info["value"] = node.value
            
        return info

    @staticmethod
    def _build_node(node: Optional[ast.AST]) -> Optional[Leaf]:
        """Recursively build Tree node from AST node."""
        if not node or not hasattr(node, "__class__"):
            return None

        position = ASTBuilder._get_position(node)
        info = ASTBuilder._get_node_info(node)
        leaf = Leaf(position, info)

        # Get child nodes based on node type
        node_type = node.__class__.__name__
        if node_type in NODES:
            child_attrs = NODES[node_type]
            for attr in child_attrs:
                value = getattr(node, attr, None)
                if value is None:
                    continue

                if isinstance(value, list):
                    for item in value:
                        child = ASTBuilder._build_node(item)
                        if child:
                            leaf.add_child(child)
                else:
                    child = ASTBuilder._build_node(value)
                    if child:
                        leaf.add_child(child)

        return leaf
