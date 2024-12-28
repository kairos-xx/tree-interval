"""
Frame analyzer module for locating current frame nodes in AST.
"""
from inspect import getsource
from typing import Optional

from .ast_builder import AstTreeBuilder
from .interval_core import Leaf
from .interval_core import Tree

class FrameAnalyzer:
    def __init__(self, frame) -> None:
        self.frame = frame
        self.ast_builder = AstTreeBuilder(frame)

    def find_current_node(self) -> Optional[Leaf]:
        """Find the AST node corresponding to current frame position."""
        tree = self.build_tree()
        if not tree or not tree.root:
            return None

        frame_first_line = self.frame.f_code.co_firstlineno
        current_line = self.frame.f_lineno - frame_first_line + 1

        line_positions = self.ast_builder._calculate_line_positions()
        
        if 0 <= current_line - 1 < len(line_positions):
            start, end = line_positions[current_line - 1]
            return tree.find_best_match(start, end)
        return None

    def build_tree(self) -> Optional[Tree]:
        """Build a complete tree from the frame's AST."""
        tree = self.ast_builder.build_from_frame()
        
        if tree and tree.root:
            line_positions = self.ast_builder._calculate_line_positions()
            nodes_by_pos = {}            
            # First pass: Update all node positions
            for node in tree.flatten():
                if hasattr(node, 'ast_node'):
                    pos = self.ast_builder._get_node_position(node.ast_node, line_positions)
                    if pos:
                        node.position = pos
                        nodes_by_pos[(pos.start, pos.end)] = node
                        print(node.selected)
            
            # Second pass: Build parent-child relationships
            sorted_positions = sorted(nodes_by_pos.keys(), key=lambda x: (x[0], -x[1]))
            for start, end in sorted_positions:
                current_node = nodes_by_pos[(start, end)]
                # Find the smallest containing interval
                for parent_start, parent_end in sorted_positions:
                    if (parent_start <= start and parent_end >= end and 
                        (parent_start, parent_end) != (start, end)):
                        parent_node = nodes_by_pos[(parent_start, parent_end)]
                        if not any(p for p in parent_node.get_ancestors() 
                                 if p.start <= start and p.end >= end):
                            parent_node.add_child(current_node)
                            break
        return tree