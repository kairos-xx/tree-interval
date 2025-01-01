"""
Frame Analysis Module.

This module provides functionality for analyzing Python stack frames
and converting them into tree structures. It bridges runtime execution
with static code analysis.
"""

from ast import AST
from inspect import isframe
from types import FrameType
from typing import Optional, cast

from .ast_builder import AstTreeBuilder
from .interval_core import Leaf, Position, Tree


class FrameAnalyzer:
    """
    Analyzes a Python stack frame to identify the corresponding AST node.

    Attributes:
        frame: The Python stack frame to analyze.
        frame_position: Position object for frame's start and end positions.
        ast_builder: AstTreeBuilder instance for AST tree construction.
        tree: The resulting AST tree built from the frame.
        current_node: The currently identified AST node within the tree.
    """

    def __init__(self, frame: Optional[FrameType]):
        """Initializes FrameAnalyzer with a given frame."""
        self.frame = frame
        # Initialize position and builder
        self.frame_position = (
            Position(0, 0) if (frame is None) else Position(self.frame)
        )
        if isframe(frame):
            # Initialize AST builder
            self.ast_builder = AstTreeBuilder(frame)
        else:
            self.ast_builder = None
        self.tree = None  # Initialize tree as None.
        self.current_node = None  # Initialize current node as None.
        self.build_tree_done = False  # Tree building not done initially.

    def find_current_node(self) -> Optional[Leaf]:
        """Find the AST node for current frame's position in the code."""
        # Build the tree if it has not been done yet.
        if not self.build_tree_done:
            self.build_tree()
        # Return None if tree or its root is unavailable.
        if not self.tree or not self.tree.root:
            return None
        if self.current_node is None:
            matching_nodes = []  # List to store matching nodes.
            for node in self.tree.flatten():
                if hasattr(node, "position") and node.position:
                    start_diff = abs(
                        node.position.start - self.frame_position.start
                    )
                    end_diff = abs(node.position.end - self.frame_position.end)
                    matching_nodes.append((node, start_diff + end_diff))

            # Find the node with the minimal position difference.
            if matching_nodes:
                self.current_node = min(matching_nodes, key=lambda x: x[1])[0]
        return self.current_node

    def build_tree(self) -> Optional[Tree]:
        """
        Builds a complete AST tree from the frame's AST.

        Returns:
            Optional[Tree]: The complete AST tree, or None if
            construction fails.
        """
        self.build_tree_done = True  # Mark tree building as done.
        if (
            not hasattr(self, "tree") or self.tree is None
        ) and self.ast_builder is not None:
            # Use builder to construct the tree
            self.tree = self.ast_builder.build_from_frame()
            # Return None if construction fails
            if not self.tree:
                return None
        if not hasattr(self, "current_node") or self.current_node is None:
            # Identify current node if not already done.
            self.find_current_node()
        if self.tree and self.tree.root and self.ast_builder:
            nodes_by_pos = {}  # Dictionary to map positions to nodes.
            for node in self.tree.flatten():
                if hasattr(node, "ast_node") and isinstance(
                    node.ast_node, AST
                ):
                    pos = self.ast_builder._get_node_position(
                        cast(AST, node.ast_node)
                    )
                    if pos:
                        # Propagate selection info
                        pos.selected = node.selected
                        node.position = pos  # Set node position.
                        nodes_by_pos[(pos.start, pos.end)] = node

            sorted_positions = sorted(
                nodes_by_pos.keys(), key=lambda x: (x[0], -x[1])
            )

            for start, end in sorted_positions:
                current_node = nodes_by_pos[(start, end)]
                if current_node.match(self.current_node):
                    current_node.selected = True  # Mark as selected

                for parent_start, parent_end in sorted_positions:
                    if (
                        # Check if the node can be a child of the parent node.
                        parent_start <= start
                        and parent_end >= end
                        and (parent_start, parent_end) != (start, end)
                    ):
                        parent_node = nodes_by_pos[(parent_start, parent_end)]
                        if not any(
                            p
                            for p in parent_node.get_ancestors()
                            if p.start <= start and p.end >= end
                        ):
                            parent_node.add_child(current_node)
                            break

        return self.tree
