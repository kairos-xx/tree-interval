
import ast
from typing import Any, Optional
from main import Tree, Leaf

class AstTreeBuilder:
    def __init__(self, frame) -> None:
        self.frame = frame
        self.source = None
        self._get_source()
        
    def _get_source(self) -> None:
        try:
            self.source = ast.unparse(ast.parse(self.frame.f_code.co_code))
        except:
            # Fallback to frame source if available
            if self.frame.f_code.co_firstlineno:
                import inspect
                self.source = inspect.getsource(self.frame.f_code)
    
    def build(self) -> Tree[str]:
        if not self.source:
            raise ValueError("No source code available")
        
        tree = ast.parse(self.source)
        result_tree = Tree[str](self.source)
        
        # Create root node from the Module
        root = Leaf(0, len(self.source), "Module")
        result_tree.root = root
        
        for node in ast.walk(tree):
            if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                # Convert line numbers to absolute positions in source
                start = self._line_col_to_pos(node.lineno, node.col_offset)
                end = self._line_col_to_pos(node.end_lineno, node.end_col_offset)
                
                if start is not None and end is not None:
                    leaf = Leaf(start, end, node.__class__.__name__)
                    result_tree.add_leaf(leaf)
        
        return result_tree
    
    def _line_col_to_pos(self, line: int, col: int) -> Optional[int]:
        """Convert line and column numbers to absolute position in source."""
        try:
            lines = self.source.splitlines(True)  # Keep line endings
            pos = 0
            for i in range(line - 1):
                pos += len(lines[i])
            return pos + col
        except:
            return None
