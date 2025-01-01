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

        # If the frame is not already a frame object, get the caller's frame
        # by traversing the call stack. This is necessary to understand the
        # context in which the attribute is being accessed or modified.
        if not isframe(frame):
            frame = stack()[(frame + 1) if isinstance(frame, int) else 2].frame
        
        # Temporarily suppress traceback output to clean up error messages that
        # will be generated for attribute access.
        original_tracebacklimit = getattr(sys, "tracebacklimit", -1)
        sys.tracebacklimit = 0
        
        # Preparing the attribute error message that will be shown if the attribute
        # is not found. The header indicates the attribute's name, and the footer
        # provides context about where in the code the error happened.
        header = "Attribute \033[1m" + name + "\033[0m not found "
        footer = indent(
            f'File "{frame.f_code.co_filename}"'
            + f"line {frame.f_lineno}, in "
            + frame.f_code.co_name,
            "   ",
        )
        new = AttributeError(f"{header}\n{footer}")

        # Use a FrameAnalyzer to inspect the current frame and find
        # the current node of execution. This helps determine if we are
        # performing an attribute setting operation.
        current_node = FrameAnalyzer(frame).find_current_node()
        if current_node:
            # If a current node is found in the frame analyzer,
            # we check if the top statement of the current node
            # has an attribute `is_set` and whether it's true,
            # indicating if an attribute assignment is being performed.
            if getattr(current_node.top_statement, "is_set", False):
                # Restore the original traceback limit before making changes.
                sys.tracebacklimit = original_tracebacklimit
                # If the attribute is being set, return a new instance
                # of the type if no specific return value is provided.
                new = type(instance)() if new_return is None else new_return
                # Set the new attribute on the instance.
                setattr(instance, name, new)
                return new
            else:
                # Construct a more informative AttributeError if the
                # attribute is accessed but not set, by using information
                # from the current node's statement.
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

        # Raise the constructed AttributeError if attribute access
        # or modification is invalid in the current context.
        raise new