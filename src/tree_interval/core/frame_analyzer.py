
"""
Frame analyzer module for locating current frame nodes in AST.
"""

from inspect import getsource
from typing import Optional

from .interval_core import Leaf, Tree
from .ast_builder import AstTreeBuilder

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
        return self.ast_builder.build_from_frame()
