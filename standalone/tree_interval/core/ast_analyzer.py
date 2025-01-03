
"""AST Analysis functionality for tree-interval package."""

import ast
from typing import Any, Dict, List, Optional, Union

from tree_interval.core.interval_core import Leaf, Position, Tree

class AstAnalyzer:
    """Analyzer for Python Abstract Syntax Trees."""
    
    def __init__(self, tree: Tree) -> None:
        """Initialize AST analyzer with a tree.
        
        Args:
            tree: Tree structure to analyze
        """
        self.tree = tree
        self.ast_cache: Dict[int, ast.AST] = {}

    def get_ast_node(self, leaf: Leaf) -> Optional[ast.AST]:
        """Get AST node for a leaf."""
        if not hasattr(leaf, 'ast_node'):
            return None
        return leaf.ast_node

    def find_assignments(self) -> List[Leaf]:
        """Find all assignment nodes."""
        return [
            leaf for leaf in self.tree.flatten()
            if isinstance(self.get_ast_node(leaf), (ast.Assign, ast.AnnAssign, ast.AugAssign))
        ]

    def find_functions(self) -> List[Leaf]:
        """Find all function definitions."""
        return [
            leaf for leaf in self.tree.flatten()
            if isinstance(self.get_ast_node(leaf), ast.FunctionDef)
        ]

    def find_classes(self) -> List[Leaf]:
        """Find all class definitions."""
        return [
            leaf for leaf in self.tree.flatten()
            if isinstance(self.get_ast_node(leaf), ast.ClassDef)
        ]

    def get_function_args(self, func_leaf: Leaf) -> List[str]:
        """Get function arguments."""
        node = self.get_ast_node(func_leaf)
        if not isinstance(node, ast.FunctionDef):
            return []
        return [arg.arg for arg in node.args.args]

    def get_function_body(self, func_leaf: Leaf) -> List[Leaf]:
        """Get function body statements."""
        return [
            child for child in func_leaf.children
            if isinstance(self.get_ast_node(child), ast.stmt)
        ]

    def analyze_complexity(self, leaf: Leaf) -> Dict[str, int]:
        """Analyze code complexity metrics."""
        complexity = {
            'lines': 0,
            'branches': 0,
            'returns': 0,
            'calls': 0
        }
        
        node = self.get_ast_node(leaf)
        if not node:
            return complexity

        for child in ast.walk(node):
            if isinstance(child, ast.If):
                complexity['branches'] += 1
            elif isinstance(child, ast.Return):
                complexity['returns'] += 1
            elif isinstance(child, ast.Call):
                complexity['calls'] += 1

        if hasattr(leaf.position, 'lineno') and hasattr(leaf.position, 'end_lineno'):
            complexity['lines'] = leaf.position.end_lineno - leaf.position.lineno + 1

        return complexity

    def find_dependencies(self, leaf: Leaf) -> List[str]:
        """Find module dependencies."""
        deps = []
        node = self.get_ast_node(leaf)
        if not node:
            return deps

        for child in ast.walk(node):
            if isinstance(child, ast.Import):
                deps.extend(name.name for name in child.names)
            elif isinstance(child, ast.ImportFrom):
                if child.module:
                    deps.append(child.module)
        return deps

    def find_attribute_accesses(self, leaf: Leaf) -> List[str]:
        """Find all attribute accesses."""
        accesses = []
        node = self.get_ast_node(leaf)
        if not node:
            return accesses

        for child in ast.walk(node):
            if isinstance(child, ast.Attribute):
                accesses.append(child.attr)
        return accesses
