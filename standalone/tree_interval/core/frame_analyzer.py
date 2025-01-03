"""Frame Analysis Module for Tree Interval.

This module provides functionality for analyzing Python stack frames
and building AST trees from the current execution context.
"""

import ast
import inspect
from typing import Any, Optional, Tuple, cast

from tree_interval.core.ast_builder import AstTreeBuilder
from tree_interval.core.interval_core import Leaf, Tree


def _get_frame_source(frame: inspect.FrameInfo) -> Tuple[str, int]:
    """Get source code and line number from frame.

    Args:
        frame: Frame to analyze

    Returns:
        Tuple of source code and start line number
    """
    try:
        lines, start_line = inspect.getsourcelines(frame.frame)
        return "".join(lines), start_line
    except (IOError, TypeError):
        return "", 1


class FrameAnalyzer:
    """Analyzer for Python stack frames."""

    def __init__(self, frame: Optional[inspect.FrameInfo] = None) -> None:
        """Initialize frame analyzer.

        Args:
            frame: Frame to analyze, uses current frame if None
        """
        self.frame = frame or inspect.currentframe()
        if not self.frame:
            return

        self.source, self.start_lineno = _get_frame_source(self.frame)
        self.builder = AstTreeBuilder(self.source, self.start_lineno)
        self.tree = self.builder.build()

    def build_tree(self) -> Optional[Tree]:
        """Build AST tree from frame source.

        Returns:
            Built tree or None if building fails
        """
        if not self.frame:
            return None
        return self.builder.build()

    def find_current_node(self) -> Optional[Leaf]:
        """Find the AST node for current execution point.

        Returns:
            Current AST node or None if not found
        """
        if not self.frame or not self.tree or not self.tree.root:
            return None

        lineno = self.frame.frame.f_lineno
        col_offset = 0

        # Find nodes matching current line
        candidates = []
        for node in self.tree.flatten():
            if (hasattr(node, "lineno") and node.lineno == lineno) or (
                hasattr(node, "end_lineno") and node.end_lineno == lineno
            ):
                candidates.append(node)

        if not candidates:
            return None

        # Find best matching node by column offset
        best_match = None
        min_distance = float("inf")
        for node in candidates:
            if not hasattr(node, "col_offset"):
                continue
            distance = abs(node.col_offset - col_offset)
            if distance < min_distance:
                min_distance = distance
                best_match = node

        return best_match