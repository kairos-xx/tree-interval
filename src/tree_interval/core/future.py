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

        if not isframe(frame):
            frame = stack()[(frame + 1) if isinstance(frame, int) else 2].frame
        original_tracebacklimit = getattr(sys, "tracebacklimit", -1)
        sys.tracebacklimit = 0
        header = "Attribute \033[1m" + name + "\033[0m not found "
        footer = indent(
            f'File "{frame.f_code.co_filename}"'
            + f"line {frame.f_lineno}, in "
            + frame.f_code.co_name,
            "   ",
        )
        new = AttributeError(f"{header}\n{footer}")
        current_node = FrameAnalyzer(frame).find_current_node()
        if current_node:
            if getattr(current_node.top_statement, "is_set", False):
                sys.tracebacklimit = original_tracebacklimit
                new = type(instance)() if new_return is None else new_return
                setattr(instance, name, new)
                return new
            else:
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

        raise new
