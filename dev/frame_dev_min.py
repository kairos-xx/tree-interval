import sys
from inspect import stack
from textwrap import indent
from typing import Any, Optional, TypeVar

from tree_interval.core.frame_analyzer import FrameAnalyzer

T = TypeVar('T')


class Nested:

    def __init__(self) -> None:
        self.__dict__: dict[str, "Nested"] = {}

    def make_tree(self, name: str, new_return: Optional[Any] = None) -> Any:
        frame = stack()[2].frame
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
                new = type(self)() if new_return is None else new_return
                setattr(self, name, new)
                return new
            else:
                statement = current_node.statement
                new = AttributeError(header + 'in \033[1m' +
                                     statement.before.replace(" ", "").replace(
                                         "\n", "").removesuffix(".") +
                                     '\033[0m\n' + footer + "\n" +
                                     indent(statement.text, '   '))
        raise new

    def __getattr__(self, name: str) -> Any:
        return self.make_tree(name, new_return=type(self)())


def xpto():
    a = Nested()
    a.b.c.d = 3
    print(a.b.c.f.g)


#print(a.c)
xpto()
