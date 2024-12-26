"""
Frame analyzer module for locating current frame nodes in AST.
"""

import ast
from inspect import getsource
from typing import Optional, Tuple

from .interval_core import Tree, Leaf, Position


class FrameAnalyzer:
    def __init__(self, frame) -> None:
        self.frame = frame
        self.source = self._extract_source()
        self.ast_tree = None if not self.source else ast.parse(self.source)
        self.line_positions = self._calculate_line_positions()

    def _extract_source(self) -> Optional[str]:
        """Extract source code from frame."""
        try:
            return getsource(self.frame.f_code)
        except (OSError, TypeError):
            return None

    def _calculate_line_positions(self) -> list[Tuple[int, int]]:
        """Calculate start and end positions for each line."""
        if not self.source:
            return []
        
        positions = []
        start = 0
        lines = self.source.splitlines(keepends=True)
        
        for line in lines:
            positions.append((start, start + len(line)))
            start += len(line)
            
        return positions

    def _get_node_position(self, node: ast.AST) -> Optional[Position]:
        """Get position information for an AST node."""
        if not hasattr(node, 'lineno'):
            return None

        try:
            start_line = node.lineno - 1  # Convert to 0-based index
            end_line = getattr(node, 'end_lineno', node.lineno) - 1
            
            if 0 <= start_line < len(self.line_positions):
                start_pos = self.line_positions[start_line][0]
                end_pos = self.line_positions[end_line][1]
                
                position = Position(start_pos, end_pos, node.__class__.__name__)
                position.lineno = node.lineno
                position.end_lineno = getattr(node, 'end_lineno', node.lineno)
                position.col_offset = getattr(node, 'col_offset', 0)
                position.end_col_offset = getattr(node, 'end_col_offset', None)
                
                return position
        except (IndexError, AttributeError):
            pass
            
        return None

    def find_current_node(self) -> Optional[Leaf]:
        """Find the AST node corresponding to current frame position."""
        if not self.source or not self.ast_tree:
            return None

        current_line = self.frame.f_lineno
        for node in ast.walk(self.ast_tree):
            if hasattr(node, 'lineno'):
                if node.lineno == current_line:
                    position = self._get_node_position(node)
                    if position:
                        return Leaf(position)
                        
        return None

    def build_tree(self) -> Optional[Tree]:
        """Build a complete tree from the frame's AST."""
        if not self.source or not self.ast_tree:
            return None

        tree = Tree(self.source)
        root_pos = Position(0, len(self.source), "Module")
        tree.root = Leaf(root_pos)

        for node in ast.walk(self.ast_tree):
            position = self._get_node_position(node)
            if position:
                tree.add_leaf(Leaf(position))

        return tree

def demonstrate_frame_analyzer():
    print("\n=== Frame Analyzer Demo ===")
    import sys
    
    def sample_code():
        a = 1
        b = 2
        c = a + b
        return c
    
    # Get current frame
    frame = sys._getframe()
    analyzer = FrameAnalyzer(frame)
    node = analyzer.find_current_node()
    
    if node:
        print(f"Found node: {node.position}")
    else:
        print("No node found.")

    tree = analyzer.build_tree()
    if tree:
        print(f"Tree built: {tree.source}")
    else:
        print("Tree not built.")


if __name__ == "__main__":
    demonstrate_frame_analyzer()