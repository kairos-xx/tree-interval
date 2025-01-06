
"""AST tree builder implementation."""
from ast import AST, NodeVisitor, parse
from contextlib import suppress
from inspect import currentframe, getframeinfo
from typing import Any, Dict, Optional, Union

from .interval_core import Leaf, Position, Tree


class AstTreeBuilder(NodeVisitor):
    """Build interval tree from Python AST nodes.

    Constructs a tree structure that maintains node positions and relationships.
    """

    def __init__(self, source: str) -> None:
        """Initialize AST tree builder.

        Args:
            source: Source code string to parse.
        """
        self.source = source.strip()
        self.ast = None
        self.tree = Tree("AST Tree")
        self.current_parent = None
        with suppress(Exception):
            self.ast = parse(self.source)

    def build(self) -> Optional[Tree]:
        """Build tree from AST.

        Returns:
            Tree: The constructed tree or None if failed.
        """
        if not self.ast:
            return None
        self.visit(self.ast)
        return self.tree

    def generic_visit(self, node: AST) -> None:
        """Process an AST node and add to tree.

        Args:
            node: AST node to process.
        """
        if not hasattr(node, "lineno"):
            return super().generic_visit(node)

        # Create position from node location
        pos = Position(
            node.col_offset if hasattr(node, "col_offset") else 0,
            node.end_col_offset if hasattr(node, "end_col_offset") else 0,
        )
        pos.lineno = node.lineno
        pos.end_lineno = (
            node.end_lineno if hasattr(node, "end_lineno") else node.lineno
        )

        # Create node info
        info: Dict[str, Any] = {"type": node.__class__.__name__}
        
        # Add special fields
        for field in ["name", "id", "arg", "func", "attr"]:
            if hasattr(node, field):
                info[field] = getattr(node, field)

        # Create leaf and add to tree
        leaf = Leaf(pos, info)
        leaf.ast_node = node

        if not self.tree.root:
            self.tree.root = leaf
            self.current_parent = leaf
        else:
            if not self.current_parent:
                self.current_parent = self.tree.root
            old_parent = self.current_parent
            self.tree.add_leaf(leaf)
            self.current_parent.add_child(leaf) 
            self.current_parent = leaf

            # Visit children
            super().generic_visit(node)
            
            # Restore parent
            self.current_parent = old_parent

def get_ast_info(
    frame: Optional[Union[int, "FrameType"]] = None,
) -> Dict[str, Any]:
    """Extract AST information from a frame.

    Args:
        frame: Frame to analyze, or stack level if int.
    
    Returns:
        Dict with AST analysis results.
    """
    if not frame:
        frame = currentframe().f_back
    if isinstance(frame, int):
        frame = currentframe(frame)

    info = getframeinfo(frame)
    builder = AstTreeBuilder(info.code_context[0])
    tree = builder.build()

    return {
        "tree": tree,
        "filename": info.filename,
        "lineno": info.lineno,
        "code": info.code_context[0] if info.code_context else "",
    }
