
"""Chain analysis module for attribute access patterns.

This module provides functionality to analyze attribute chains in Python code,
particularly for determining whether attributes should be created or accessed.
It parses Python expressions to extract information about attribute chains
and their usage context.
"""

import ast
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ChainInfo:
    """Information about an attribute access chain.

    Tracks whether the chain is part of an assignment operation and stores the
    sequence of attribute names in the chain.

    Attributes:
        is_assignment: True if chain appears in assignment context
        chain: List of attribute names in access order
        assignment_type: Type of assignment ('Assign', 'Add', etc) or None
    """
    is_assignment: bool
    chain: List[str]
    assignment_type: Optional[str]


class ChainAnalyzer:
    """Analyzes attribute chains and their assignment/access patterns.

    This class provides static methods for parsing Python code to extract
    information about attribute chains, particularly useful for determining
    whether attributes should be created dynamically.
    """

    @staticmethod
    def parse_expression(code: str) -> ChainInfo:
        """Parse code and analyze the attribute chain structure.

        Takes a string of Python code and extracts information about any
        attribute chains, including:
        - Whether it's an assignment operation
        - The sequence of attributes accessed
        - The type of assignment if applicable

        Args:
            code: Python code string to analyze

        Returns:
            ChainInfo containing the analysis results

        Example:
            >>> info = ChainAnalyzer.parse_expression("obj.a.b.c = 42")
            >>> print(info.chain)  # ['obj', 'a', 'b', 'c']
            >>> print(info.is_assignment)  # True
        """
        try:
            tree = ast.parse(code)
            node = (tree.body[0].value if isinstance(tree.body[0], ast.Expr)
                   else tree.body[0])

            # Handle augmented assignments (+=, -=, etc)
            if isinstance(node, ast.AugAssign):
                target = node.target
                op_type = type(node.op).__name__
                chain = []
                while isinstance(target, ast.Attribute):
                    chain.append(target.attr)
                    target = target.value
                if isinstance(target, ast.Name):
                    chain.append(target.id)
                chain.reverse()
                return ChainInfo(True, chain, op_type)

            # Handle normal assignments
            elif isinstance(node, ast.Assign):
                target = node.targets[0]
                chain = []
                while isinstance(target, ast.Attribute):
                    chain.append(target.attr)
                    target = target.value
                if isinstance(target, ast.Name):
                    chain.append(target.id)
                chain.reverse()
                return ChainInfo(True, chain, 'Assign')

            # Handle attribute access without assignment
            elif isinstance(node, ast.Attribute):
                chain = []
                current = node
                while isinstance(current, ast.Attribute):
                    chain.append(current.attr)
                    current = current.value
                if isinstance(current, ast.Name):
                    chain.append(current.id)
                chain.reverse()
                return ChainInfo(False, chain, None)

        except Exception:
            # Return empty chain info for unparseable code
            return ChainInfo(False, [], None)

        return ChainInfo(False, [], None)

    @staticmethod
    def should_create_attr(code: str, name: str) -> bool:
        """Determine if an attribute should be created dynamically.

        Analyzes the code context to decide whether an attribute should be
        created during attribute chain resolution.

        Args:
            code: The Python code context string
            name: The attribute name being checked

        Returns:
            bool: True if the attribute should be created

        Example:
            >>> ChainAnalyzer.should_create_attr("obj.a.b.c = 42", "a")
            True  # 'a' appears before final position in assignment
        """
        info = ChainAnalyzer.parse_expression(code)
        return info.is_assignment and name in info.chain[:-1]
