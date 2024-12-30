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

    def __getattr__(self, name: str) -> "Nested":
        caller = stack()[1]
        is_set = False
        underline_text = ""
        before = ""
        analyzer = FrameAnalyzer(caller.frame)
        current_node = analyzer.find_current_node()
        tree = analyzer.build_tree()
        print(caller.positions,current_node.position.position_as("position"))
        if current_node and tree:
            top_statement=current_node.top_statement
            parent=current_node.parent
            print(parent)
            for node in tree.flatten():
                if node.match(parent):
                    node.style = LeafStyle(color="#0000ff", bold=True)
                if node.match(top_statement):
                    node.style = LeafStyle(color="#00ff00", bold=True)
                if node.match(current_node):
                    node.style = LeafStyle(color="#ff0000", bold=True)
            tree.visualize()
            is_set = getattr(top_statement, "is_set", False)
            statement = current_node.statement
            underline_text = statement.text
            before = statement.before.replace(" ",
                                              "").replace("\n",
                                                          "").removesuffix(".")
        if is_set:
            new = type(self)()
            setattr(self, name, new)
            return new
        else:
            import sys
            sys.tracebacklimit = 0
            raise AttributeError(
                f"Attribute \033[1m{name}\033[0m not found in " +
                f"\033[1m{before}\033[0m\n" +
                f"   File \"{caller.filename}\"," +
                f"line {caller.lineno}, in {caller.function}\n" +
                f"{indent(underline_text,'   ')}")


#def test():
print(f"test")
a = Nested()
a.b.c.d.e.f.g.g.g = 3
print((a.b.c.e.f.g))

#test()
