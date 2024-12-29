"""
Frame Analysis Module.

This module provides functionality for analyzing Python stack frames and converting them
into tree structures. It bridges runtime execution context with static code analysis.

Key Components:
    - FrameAnalyzer: Main class for converting stack frames to tree structures
    - Frame position tracking: Maps runtime positions to source code
    - AST integration: Connects frame analysis with abstract syntax trees

Technical Details:
    - Uses inspect module for frame introspection
    - Maintains source code position awareness
    - Integrates with AST analysis for deeper code understanding
    - Provides runtime context for visualization

Usage Example:
    analyzer = FrameAnalyzer(current_frame)
    node = analyzer.find_current_node()
    tree = analyzer.build_tree()
"""

from ast import AST
from typing import Optional, cast

from .ast_builder import AstTreeBuilder
from .interval_core import Leaf, Position, Tree


class FrameAnalyzer:
    """
    Analyzes a Python stack frame to identify the corresponding Abstract Syntax Tree (AST) node.

    Attributes:
        frame: The Python stack frame to analyze.
        frame_position: Position object representing the start and end positions of the frame.
        ast_builder: AstTreeBuilder instance for constructing the AST tree.
        tree: The resulting AST tree built from the frame.
        current_node: The currently identified AST node within the tree.
    """

    def __init__(self, frame) -> None:
        """Initializes FrameAnalyzer with a given frame."""
        self.frame = frame
        self.frame_position = Position(self.frame) #Creates a Position object from the frame
        self.ast_builder = AstTreeBuilder(frame) #Builds an AST tree from the frame
        self.tree = None # Initialize the tree to None
        self.current_node = None # Initialize the current node to None

    def find_current_node(self) -> Optional[Leaf]:
        """
        Finds the AST node corresponding to the current frame's position.

        Returns:
            Optional[Leaf]: The AST node at the current frame position, or None if not found.
        """
        # Build the tree if it hasn't been built yet.
        self.tree = self.tree or self.build_tree()
        #If the tree is empty or root is None, return None
        if not self.tree or not self.tree.root:
            return None
        #If the current node is not found yet then we search for it
        if self.current_node is None:
            self.current_node = self.tree.find_best_match(
                self.frame_position.start, self.frame_position.end) #Find best match for the current frame position
        return self.current_node #Return the current node

    def build_tree(self) -> Optional[Tree]:
        """
        Builds a complete AST tree from the frame's AST.

        Returns:
            Optional[Tree]: The complete AST tree, or None if construction fails.
        """
        # Builds the tree using the ast_builder
        self.tree = self.ast_builder.build_from_frame()
        # Finds the current node, if not already found.
        self.current_node = self.current_node or self.find_current_node()
        #If the tree is built and root exists
        if self.tree and self.tree.root:
            line_positions = self.ast_builder._calculate_line_positions() # Calculates line positions for nodes
            nodes_by_pos = {} # Dictionary to store nodes by their positions
            # First pass: Update all node positions
            for node in self.tree.flatten(): #Iterate through all nodes in the tree
                if hasattr(node, "ast_node") and isinstance(
                        node.ast_node, AST): #Checks if the node has an ast_node attribute and is an instance of AST
                    pos = self.ast_builder._get_node_position(
                        cast(AST, node.ast_node), line_positions) #Gets node position using ast_builder
                    if pos: #If position is found
                        pos.selected = node.selected #Sets selected attribute of the position
                        node.position = pos #Sets position of the node
                        nodes_by_pos[(pos.start, pos.end)] = node #Adds node to the dictionary

            # Second pass: Build parent-child relationships
            sorted_positions = sorted(nodes_by_pos.keys(),
                                      key=lambda x: (x[0], -x[1])) #Sorts positions by start and end
            for start, end in sorted_positions: #Iterate through sorted positions
                current_node = nodes_by_pos[(start, end)] #Gets current node from dictionary
                #Checks if current node matches the selected node
                if current_node.match(self.current_node):
                    current_node.selected = True #Sets selected attribute of the node to True
                # Find the smallest containing interval
                for parent_start, parent_end in sorted_positions: #Iterate through sorted positions
                    #Checks if the current node is contained within the parent node
                    if (parent_start <= start and parent_end >= end
                            and (parent_start, parent_end) != (start, end)):
                        parent_node = nodes_by_pos[(parent_start, parent_end)] #Gets parent node from dictionary
                        #Checks if the parent node does not already have a child that contains the current node
                        if not any(p for p in parent_node.get_ancestors()
                                   if p.start <= start and p.end >= end):
                            parent_node.add_child(current_node) #Adds current node as a child of the parent node
                            break #Break out of the loop after adding the child
        return self.tree #Return the tree

from inspect import currentframe
analyzer = FrameAnalyzer(currentframe())
node = analyzer.find_current_node()  # Get current execution point
tree = analyzer.build_tree()         # Build full AST representation