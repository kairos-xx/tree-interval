from ast import AST, unparse
from inspect import stack
from typing import Any

from tree_interval.core.frame_analyzer import FrameAnalyzer
from tree_interval.core.interval_core import LeafStyle


class Nested:

    def __init__(self) -> None:
        # Tell type checker that this is a dynamic class
        self.__dict__: dict[str, "Nested"] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def __getattr__(self, name: str) -> "Nested":
        print(f'\n{"#"*50}')
        print(f"attribute name: {name}")
        analyzer = FrameAnalyzer(stack()[1].frame)
        current_node = analyzer.find_current_node()
        tree = analyzer.build_tree()
        continues = False
        is_set = False
        underline_text = ""
        before = ""
        if current_node and tree:
            current_node_ast_node = getattr(current_node, "ast_node", None)
            print("Current attribute node: " +
                  (unparse(current_node_ast_node) if isinstance(
                      current_node_ast_node, AST) else "None"))
            top_statement = current_node.top_statement
            top_statement_ast_node = getattr(top_statement, "ast_node", None)
            print("Top attribute node: " +
                  (unparse(top_statement_ast_node) if isinstance(
                      top_statement_ast_node, AST) else "None"))
            is_set = top_statement.is_set if top_statement else False
            print(f"Is set operation: {is_set}")
            next_attribute = current_node.next_attribute
            continues = bool(next_attribute)
            next_attribute_ast_node = getattr(next_attribute, "ast_node", None)
            print("Next attribute node: " +
                  (unparse(next_attribute_ast_node) if isinstance(
                      next_attribute_ast_node, AST) else "None"))

            previous_attribute = current_node.previous_attribute
            previous_attribute_ast_node = getattr(previous_attribute,
                                                  "ast_node", None)
            print("Previous attribute node: " +
                  (unparse(previous_attribute_ast_node) if isinstance(
                      previous_attribute_ast_node, AST) else "None"))

            # Show statement with different marker styles
            print("\nDefault markers:", current_node.statement)
            underline_text = current_node.statement.as_text()
            before = current_node.statement.before.removesuffix(".")

            # print(current_node.statement)
            flat_nodes = tree.flatten()
            for node in flat_nodes:
                if node.match(current_node):
                    node.style = LeafStyle(color="#ff0000", bold=True)
                elif node.match(top_statement):
                    node.style = LeafStyle(color="#00ff00", bold=False)
                elif node.match(next_attribute):
                    node.style = LeafStyle(color="#0000ff", bold=False)
                else:
                    node.style = LeafStyle(color="#cccccc", bold=False)
            tree.visualize()

        print(f"\nThe chain continues: {continues} |" +
              f" At the end is a set: {is_set}")

        if is_set:
            new = type(self)()
            setattr(self, name, new)
            return new
        else:
            caller = stack()[1]
            raise AttributeError(
                f"Attribute '{name}' not found (called from {caller.filename}, line {caller.lineno}, in {caller.function})")


def test():
    a = Nested()
    a.b.c = 3
    print((a.b.d.e.f.g))
    # print(a.b.c.e)


test()
