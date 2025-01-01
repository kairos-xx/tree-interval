import sys
from inspect import isframe, stack
from textwrap import indent
from types import FrameType
from typing import Any, Optional, Union

from .frame_analyzer import FrameAnalyzer


class Future:

    def __new__(cls,
                name: str,
                instance: object,
                frame: Optional[Union[int, FrameType]] = None,
                new_return: Optional[Any] = None) -> Any:

        if not isframe(frame):
            frame = stack()[(frame + 1) if isinstance(frame, int) else 2].frame
        original_tracebacklimit = getattr(sys, "tracebacklimit", -1)
        sys.tracebacklimit = 0
        header = 'Attribute \033[1m' + name + '\033[0m not found '
        footer = indent(
            f'File "{frame.f_code.co_filename}"' +
            f'line {frame.f_lineno}, in ' + frame.f_code.co_name, '   ')
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
                new = AttributeError(header + 'in \033[1m' +
                                     statement.before.replace(" ", "").replace(
                                         "\n", "").removesuffix(".") +
                                     '\033[0m\n' + footer + "\n" +
                                     indent(statement.text, '   '))

        raise new
