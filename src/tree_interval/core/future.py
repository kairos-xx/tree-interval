
"""Future attribute access handler.

Provides dynamic attribute handling with runtime introspection.
"""

from ast import AST
from contextlib import suppress 
from inspect import currentframe, stack
from textwrap import indent
from types import FrameType
from typing import Any, Optional, Union

from .frame_analyzer import FrameAnalyzer

def is_set_operation(node: Optional[AST]) -> bool:
    """Check if AST node represents a set operation.

    Args:
        node: AST node to check

    Returns:
        bool: True if node is a set operation
    """
    if not node:
        return False
    return node.__class__.__name__ == "Assign"

class Future:
    """Dynamic attribute handler with runtime introspection."""

    def __new__(
        cls,
        name: str,
        instance: Optional[object] = None,
        frame: Optional[Union[int, FrameType]] = None,
        new_return: Optional[Any] = None,
    ) -> Any:
        """Create or access dynamic attributes.

        Args:
            name: Attribute name
            instance: Object instance
            frame: Call frame or stack level
            new_return: Value for new attributes

        Returns:
            Created attribute or error

        Raises:
            AttributeError: For invalid access
        """
        if not frame:
            frame = currentframe().f_back
        elif isinstance(frame, int):
            frame = stack()[frame + 1].frame

        # Check context
        analyzer = FrameAnalyzer(frame)
        current_node = analyzer.find_current_node()

        if current_node and current_node.ast_node:
            if is_set_operation(current_node.ast_node):
                # Create new attribute
                value = new_return() if callable(new_return) else new_return
                if instance:
                    setattr(instance, name, value)
                return value
            
            # Error on invalid access
            statement = getattr(current_node, "statement", None)
            if statement:
                msg = (f"Attribute '{name}' not found in:\n"
                      f"{indent(statement.text, '  ')}")
            else:
                msg = f"Attribute '{name}' not found"
            
            raise AttributeError(msg)

        return None

