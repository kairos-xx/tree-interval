import sys
from inspect import isframe, stack
from textwrap import indent
from types import FrameType
from typing import Any, Optional, Union

from .frame_analyzer import FrameAnalyzer


class Future:
    """
    Handles dynamic attribute creation and access in nested object structures.

    This class provides context-aware attribute handling by analyzing
    the call stack and current execution frame to determine whether an
    attribute access is part of a setting operation
    (creating new attributes) or a getting operation (which may
    raise appropriate errors).

    Example:
        class Nested:
            def __getattr__(self, name):
                return Future(name, frame=1, instance=self)

        obj = Nested()
        obj.a.b.c = 42  # Creates nested structure
        print(obj.a.b.c)  # Prints 42
        print(obj.x.y)  # Raises AttributeError with context
    """

    def __new__(
        cls,
        name: str,
        instance: object,
        frame: Optional[Union[int, FrameType]] = None,
        new_return: Optional[Any] = None,
    ) -> Any:
        """Dynamic attribute creation and access handler.

        This method implements the core logic for dynamic attribute
        handling by:
        1. Analyzing call stack context to determine operation type
        2. Creating new attributes in assignment context
        3. Raising descriptive errors in access context
        4. Managing nested attribute chains

        The context analysis includes:
        - Frame inspection for operation type
        - AST analysis for statement structure
        - Position tracking for error reporting

        Args:
            name: Name of the attribute being accessed
            instance: Object instance where attribute belongs
            frame: Call frame or stack level for context
            new_return: Value to use for new attributes

        Returns:
            Any: Created attribute value in setting context

        Raises:
            AttributeError: When attribute doesn't exist in get context

        Example:
            >>> obj.nonexistent = 42  # Creates new attribute
            >>> print(obj.nonexistent)  # Prints 42
            >>> print(obj.missing)  # Raises AttributeError
        """
        """Create or handle attribute access in a dynamic object structure.

        This method provides the core functionality for dynamic attribute
        handling, determining whether to create new attributes or raise
        appropriate errors.

        Args:
            name: The attribute name being accessed or created
            instance: The object instance where the attribute belongs
            frame: Optional frame object or stack level for context analysis
            new_return: Optional value to use when creating new attributes

        Returns:
            Any: Created attribute value if in a setting context

        Raises:
            AttributeError: When attribute doesn't exist in a get context
        """
        # Get caller's frame if not provided for context analysis
        if not isframe(frame):
            frame = stack()[(frame + 1) if isinstance(frame, int) else 2].frame

        # Suppress traceback for cleaner error messages
        original_tracebacklimit = getattr(sys, "tracebacklimit", -1)
        sys.tracebacklimit = 0

        # Prepare error message components with formatting
        header = "Attribute \033[1m" + name + "\033[0m not found "
        footer = indent(
            f'File "{frame.f_code.co_filename}"'
            + f"line {frame.f_lineno}, in "
            + frame.f_code.co_name,
            "   ",
        )
        new = AttributeError(f"{header}\n{footer}")

        # Analyze current execution frame to determine context
        current_node = FrameAnalyzer(frame).find_current_node()
        if current_node:
            # Check if we're in an attribute setting operation
            if getattr(current_node.top_statement, "is_set", False):
                sys.tracebacklimit = original_tracebacklimit
                # Create and set new attribute if in setting context
                new = type(instance)() if new_return is None else new_return
                setattr(instance, name, new)
                return new
            else:
                # Build detailed error for attribute access in get context
                statement = current_node.statement
                new = AttributeError(
                    header
                    + "in \033[1m"
                    + statement.before.replace(" ", "")
                    .replace("\n", "")
                    .removesuffix(".")
                    + "\033[0m\n"
                    + footer
                    + "\n"
                    + indent(statement.text, "   ")
                )

        # Raise error for invalid attribute access
        raise new
