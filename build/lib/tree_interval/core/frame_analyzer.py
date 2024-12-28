"""
Frame analyzer module for locating current frame nodes in AST.
"""

from ast import AST
from typing import Optional, cast

from .ast_builder import AstTreeBuilder
from .interval_core import Leaf, Position, Tree


class FrameAnalyzer:

    def __init__(self, frame) -> None:
        self.frame = frame
        self.frame_position = Position(self.frame)
        self.ast_builder = AstTreeBuilder(frame)
        self.tree = None
        self.current_node = None

    def find_current_node(self) -> Optional[Leaf]:
        """Find the AST node corresponding to current frame position.

        Returns:
            Optional[Leaf]: The AST node at current frame position,
            or None if not found
        """
        self.tree = self.tree or self.build_tree()
        if not self.tree or not self.tree.root:
            return None
        if self.current_node is None:
            self.current_node = self.tree.find_best_match(
                self.frame_position.start, self.frame_position.end)
        return self.current_node

    def build_tree(self) -> Optional[Tree]:
        """Build a complete tree from the frame's AST."""
        self.tree = self.ast_builder.build_from_frame()
        self.current_node = self.current_node or self.find_current_node()
        if self.tree and self.tree.root:
            line_positions = self.ast_builder._calculate_line_positions()
            nodes_by_pos = {}
            # First pass: Update all node positions
            for node in self.tree.flatten():
                if hasattr(node, "ast_node") and isinstance(
                        node.ast_node, AST):
                    pos = self.ast_builder._get_node_position(
                        cast(AST, node.ast_node), line_positions)
                    if pos:
                        pos.selected = node.selected
                        node.position = pos
                        nodes_by_pos[(pos.start, pos.end)] = node

            # Second pass: Build parent-child relationships
            sorted_positions = sorted(nodes_by_pos.keys(),
                                      key=lambda x: (x[0], -x[1]))
            for start, end in sorted_positions:
                current_node = nodes_by_pos[(start, end)]
                if current_node.match(self.current_node):
                    current_node.selected = True
                # Find the smallest containing interval
                for parent_start, parent_end in sorted_positions:
                    if (parent_start <= start and parent_end >= end
                            and (parent_start, parent_end) != (start, end)):
                        parent_node = nodes_by_pos[(parent_start, parent_end)]
                        if not any(p for p in parent_node.get_ancestors()
                                   if p.start <= start and p.end >= end):
                            parent_node.add_child(current_node)
                            break
        return self.tree
