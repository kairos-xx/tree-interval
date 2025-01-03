
from inspect import Frame, currentframe, stack
from types import FrameType
from typing import Any, Optional, Union
from textwrap import indent
import sys

from tree_interval.core.frame_analyzer import FrameAnalyzer

class Future:
    """Handles dynamic attribute creation and access with AST analysis."""

    def __new__(
        cls,
        name: str,
        instance: object,
        frame: Optional[Union[int, FrameType]] = None,
        new_return: Optional[Any] = None,
    ) -> Any:
        if isinstance(frame, int):
            try:
                frame_info = stack()[frame]
                frame = frame_info.frame
                analyzer = FrameAnalyzer(frame_info)
            except (IndexError, AttributeError):
                frame = None
                analyzer = None
        else:
            frame = frame if isinstance(frame, Frame) else None
            analyzer = None if frame is None else FrameAnalyzer(frame)

        original_tracebacklimit = getattr(sys, "tracebacklimit", -1)
        sys.tracebacklimit = 0

        header = "Attribute \033[1m" + name + "\033[0m not found "
        footer = indent(
            f'File "{frame.f_code.co_filename}"'
            + f" line {frame.f_lineno}, in "
            + frame.f_code.co_name,
            "   ",
        )
        error = AttributeError(f"{header}\n{footer}")

        if analyzer:
            current_node = analyzer.find_current_node()
            if current_node and getattr(current_node.top_statement, "is_set", False):
                sys.tracebacklimit = original_tracebacklimit
                new = type(instance)() if new_return is None else new_return
                setattr(instance, name, new)
                return new
            elif current_node:
                statement = current_node.statement
                error = AttributeError(
                    header
                    + "in \033[1m"
                    + statement.before.replace(" ", "").replace("\n", "").removesuffix(".")
                    + "\033[0m\n"
                    + footer
                    + "\n"
                    + indent(statement.text, "   ")
                )

        raise error


class Nested:
    def __init__(self) -> None:
        self.__dict__: dict[str, "Nested"] = {}

    def __getattr__(self, name: str) -> Any:
        return Future(
            name,
            frame=stack()[1].frame,
            instance=self,
            new_return=type(self)(),
        )


def frame_function():
    a = Nested()
    a.b.c.d = 3
    print(a.b.c.d)  # Should print 3
    print(a.x.y.z)  # Should raise detailed AttributeError


if __name__ == "__main__":
    frame_function()
