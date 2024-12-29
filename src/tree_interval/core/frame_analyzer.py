"""
Frame Analysis Module.

This module provides functionality for analyzing Python stack frames
and converting them into tree structures.
It bridges runtime execution with static code analysis.
"""

from ast import AST
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

    def __init__(self, frame) -> None:
        """Initializes FrameAnalyzer with a given frame."""
        self.frame = frame
        # Creates a Position object from the frame
        self.frame_position = Position(self.frame)
        # Builds an AST tree from the frame
        self.ast_builder = AstTreeBuilder(frame)
        # Initialize the tree to None
        self.tree = None
        # Initialize the current node to None
        self.current_node = None

    def find_current_node(self) -> Optional[Leaf]:
        """
        Finds the AST node corresponding to the current frame's position.

        Returns:
            Optional[Leaf]: The AST node at the current frame position,
            or None if not found.
        """
        # Build the tree if it hasn't been built yet
        self.tree = self.tree or self.build_tree()
        # If the tree is empty or root is None, return None
        if not self.tree or not self.tree.root:
            return None
        # If the current node is not found yet then we search for it
        if self.current_node is None:
            # Find best match for the current frame position
            self.current_node = self.tree.find_best_match(
                self.frame_position.start, self.frame_position.end)
        return self.current_node

    def build_tree(self) -> Optional[Tree]:
        """
        Builds a complete AST tree from the frame's AST.

        Returns:
            Optional[Tree]: The complete AST tree, or None if
                            construction fails.
        """
        # Builds the tree using the ast_builder
        self.tree = self.ast_builder.build_from_frame()
        # Finds the current node, if not already found
        self.current_node = self.current_node or self.find_current_node()

        if self.tree and self.tree.root:
            # Calculates line positions for nodes
            line_positions = self.ast_builder._calculate_line_positions()
            # Dictionary to store nodes by their positions
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
                # Check if current node matches the selected node
                if current_node.match(self.current_node):
                    current_node.selected = True

                # Find smallest containing interval for
                # parent-child relationships
                for parent_start, parent_end in sorted_positions:
                    if (parent_start <= start and parent_end >= end
                            and (parent_start, parent_end) != (start, end)):
                        parent_node = nodes_by_pos[(parent_start, parent_end)]
                        # Check if parent doesn't have a containing ancestor
                        if not any(p for p in parent_node.get_ancestors()
                                   if p.start <= start and p.end >= end):
                            parent_node.add_child(current_node)
                            break

        return self.tree
