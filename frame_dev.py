from inspect import currentframe
from tree_interval.core.frame_analyzer import FrameAnalyzer


def analyze_this():
    analyzer = FrameAnalyzer(currentframe())

    current_node = analyzer.find_current_node()
    print("Current Node Information:")
    print(f"Node: {current_node if current_node else None}")

    tree = analyzer.build_tree()

    if current_node and tree and tree.root:
        print("\nFull AST Tree:")
        # Color nodes based on type and mark current node
        flat_nodes = tree.flatten()
        for node in flat_nodes:
            # Basic style for all nodes
            
            node.style = LeafStyle(color="#888888", bold=False)

            # Check if this is the current node by matching position and info
            if (node.start == current_node.start
                    and node.end == current_node.end
                    and str(node.info) == str(current_node.info)):
                
                node.style = LeafStyle(color="#ff0000", bold=True)
                node.selected = True
            # Check node type from info
            elif hasattr(node, "info") and isinstance(node.info, dict):
                node_type = node.info.get("name")
                if node_type == "Call":
                    
                    node.style = LeafStyle(color="#00ff00", bold=True)
                elif node_type == "FunctionDef":
                    
                    node.style = LeafStyle(color="#0000ff", bold=False)

        printer = RichTreePrinter()
        printer.print_tree(tree)
        tree.visualize()


analyze_this()
