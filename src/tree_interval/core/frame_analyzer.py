"""
Frame analyzer module for locating current frame nodes in AST.
"""

<<<<<<< HEAD
from ast import AST
from typing import Optional, cast

from .ast_builder import AstTreeBuilder
=======
from ast import AST, parse, walk
from inspect import getsource
from typing import Optional, Tuple

>>>>>>> origin/main
from .interval_core import Leaf, Position, Tree


class FrameAnalyzer:
<<<<<<< HEAD

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
=======
    def __init__(self, frame) -> None:
        self.frame = frame
        self.source = self._extract_source()
        self.ast_tree = None if not self.source else parse(self.source)
        self.line_positions = self._calculate_line_positions()

    def _extract_source(self) -> Optional[str]:
        """Extract source code from frame."""
        try:
            if self.frame and self.frame.f_code:
                source = getsource(self.frame.f_code)
                # Remove common leading whitespace
                lines = source.splitlines()
                common_indent = min(
                    len(line) - len(line.lstrip()) for line in lines if line.strip()
                )
                return "\n".join(
                    line[common_indent:] if line.strip() else line for line in lines
                )
            return None
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

    def _get_node_position(self, node: AST) -> Optional[Position]:
        """Get position information for an AST node."""
        try:
            lineno = getattr(node, "lineno", None)
            if lineno is None:
                return None

            start_line = lineno - 1  # Convert to 0-based index
            end_lineno = getattr(node, "end_lineno", lineno)
            end_line = end_lineno - 1

            if 0 <= start_line < len(self.line_positions):
                start_pos = self.line_positions[start_line][0]
                end_pos = self.line_positions[end_line][1]

                position = Position(start_pos, end_pos, node.__class__.__name__)
                position.lineno = lineno
                position.end_lineno = end_lineno
                position.col_offset = getattr(node, "col_offset", 0)
                position.end_col_offset = getattr(node, "end_col_offset", None)

                return position
        except (IndexError, AttributeError):
            pass

        return None

    def find_current_node(self) -> Optional[Leaf]:
        """Find the AST node corresponding to current frame position."""
        if not self.source or not self.ast_tree:
            return None

        # Build tree first
        tree = self.build_tree()
        if not tree or not tree.root:
            return None

        # Get current line interval
        frame_first_line = self.frame.f_code.co_firstlineno
        current_line = self.frame.f_lineno - frame_first_line + 1  # type: ignore

        # Find in line positions
        if 0 <= current_line - 1 < len(self.line_positions):
            start, end = self.line_positions[current_line - 1]  # type: ignore
            return tree.find_best_match(start, end)

        return None

    def build_tree(self) -> Optional[Tree]:
        """Build a complete tree from the frame's AST."""
        if not self.source or not self.ast_tree:
            return None

        tree = Tree(self.source)
        root_pos = Position(0, len(self.source), "Module")
        tree.root = Leaf(root_pos)

        # First pass - collect all nodes with their positions
        nodes_with_positions = []
        for node in walk(self.ast_tree):
            position = self._get_node_position(node)
            if position:
                leaf = Leaf(position)
                leaf.ast_node = node
                nodes_with_positions.append((node, leaf))

        # Second pass - build hierarchy
        for _, leaf in nodes_with_positions:
            tree.add_leaf(leaf)

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
>>>>>>> origin/main
