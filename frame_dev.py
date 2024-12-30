from ast import AST, unparse
from inspect import stack

from tree_interval.core.frame_analyzer import FrameAnalyzer
from tree_interval.core.interval_core import LeafStyle


class Nested:

    def __getattr__(self, name):
        new = type(self)()
        setattr(self, name, new)
        print(f'\n{"#"*50}')
        print(f"attribute name: {name}")
        analyzer = FrameAnalyzer(stack()[1].frame)
        current_node = analyzer.find_current_node()
        tree = analyzer.build_tree()
        if current_node and tree:
            current_node_ast_node = getattr(current_node, "ast_node", None)
            print("Current attribute node: " +
                  (unparse(current_node_ast_node) if isinstance(
                      current_node_ast_node, AST) else 'None'))
            top_statement = current_node.top_statement
            top_statement_ast_node = getattr(top_statement, "ast_node", None)
            print("Top attribute node: " +
                  (unparse(top_statement_ast_node) if isinstance(
                      top_statement_ast_node, AST) else 'None'))
            next_attribute = current_node.next_attribute
            next_attribute_ast_node = getattr(next_attribute, "ast_node", None)
            print("Next attribute node: " +
                  (unparse(next_attribute_ast_node) if isinstance(
                      next_attribute_ast_node, AST) else 'None'))
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
        return new


def analyze_this():
    a = Nested()
    a.b.c.d = 1
    print(a.b.c.e)
    # analyzer = FrameAnalyzer(currentframe())

    # current_node = analyzer.find_current_node()
    # print("Current Node Information:")
    # print(f"Node: {current_node if current_node else None}")

    # tree = analyzer.build_tree()

    # if current_node and tree and tree.root:
    #     print("\nFull AST Tree:")
    #     # Color nodes based on type and mark current node
    #     flat_nodes = tree.flatten()
    #     for node in flat_nodes:
    #         # Basic style for all nodes

    #         node.style = LeafStyle(color="#888888", bold=False)

    #         # Check if this is the current node by matching position and info
    #         if (node.start == current_node.start
    #                 and node.end == current_node.end
    #                 and str(node.info) == str(current_node.info)):

    #             node.style = LeafStyle(color="#ff0000", bold=True)
    #             node.selected = True
    #         # Check node type from info
    #         elif hasattr(node, "info") and isinstance(node.info, dict):
    #             node_type = node.info.get("name")
    #             if node_type == "Call":

    #                 node.style = LeafStyle(color="#00ff00", bold=True)
    #             elif node_type == "FunctionDef":

    #                 node.style = LeafStyle(color="#0000ff", bold=False)

    #     printer = RichTreePrinter()
    #     printer.print_tree(tree)
    #     tree.visualize()


analyze_this()
