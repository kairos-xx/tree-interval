import sys
from dis import Positions
from inspect import stack
from textwrap import indent
from typing import Any

from tree_interval.core.frame_analyzer import FrameAnalyzer
from tree_interval.core.interval_core import LeafStyle


class Nested:

    def __init__(self) -> None:
        self.__dict__: dict[str, "Nested"] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def make_tree(self, name, caller, analyzer):
        # Synchronize analyzer position with frame position before finding node
        analyzer.frame_position.lineno = caller.positions.lineno
        analyzer.frame_position.end_lineno = caller.positions.end_lineno
        analyzer.frame_position.col_offset = caller.positions.col_offset
        analyzer.frame_position.end_col_offset = caller.positions.end_col_offset
        
        tree = analyzer.build_tree()
        current_node = analyzer.find_current_node()
        
        # For debugging
        print("Frame position:", caller.positions)
        print("Node position:", Positions(
            current_node.position.lineno,
            current_node.position.end_lineno,
            current_node.position.col_offset,
            current_node.position.end_col_offset,
        ) if current_node else None)
        
        if current_node and tree:
            new = None
            top_statement = current_node.top_statement
            parent = current_node.parent
            for node in tree.flatten():
                if node.match(parent):
                    node.style = LeafStyle(color="#0000ff", bold=True)
                if node.match(top_statement):
                    node.style = LeafStyle(color="#00ff00", bold=True)
                if node.match(current_node):
                    node.style = LeafStyle(color="#ff0000", bold=True)
            tree.visualize(root=top_statement)
            if getattr(top_statement, "is_set", False):
                new = type(self)()
                setattr(self, name, new)
            statement = current_node.statement
            return (
                new,
                statement.text,
                (statement.before.replace(" ",
                                          "").replace("\n",
                                                      "").removesuffix(".")),
            )
        return None, "", ""

    def __getattr__(self, name: str) -> "Nested":
        caller = stack()[1]
        new, underline_text, before = self.make_tree(
            name, caller, FrameAnalyzer(caller.frame))
        if new:
            return new
        sys.tracebacklimit = 0
        raise AttributeError(
            f"Attribute \033[1m{name}\033[0m not found in " +
            f"\033[1m{before}\033[0m\n" + indent(
                f'File "{caller.filename}"' + f'line {caller.lineno}, in ' +
                f'{caller.function}\n ' + f'{underline_text}', '   '))

print("TEST")
a = Nested()
a.b = 3
print(a.c)
