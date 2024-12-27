
import sys
from src.tree_interval import FrameAnalyzer, VisualizationConfig

def demonstrate_frame_analyzer():
    print("\n=== Frame Analyzer Demo ===")
    
    def analyze_this():
        x = 1 + 2  # This line will be analyzed
        frame = sys._getframe()  # Get frame inside the function
        analyzer = FrameAnalyzer(frame)
        
        # Show current node
        current_node = analyzer.find_current_node()
        if current_node:
            print("Current Node Information:")
            print(f"Node: {current_node._as_dict()}")
        else:
            print("No current node found")
        
        # Build and show tree
        tree = analyzer.build_tree()
        if tree:
            print("\nFull AST Tree:")
            tree.visualize(VisualizationConfig(
                position_format='tuple',
                show_children_count=True
            ))
        return x

    # Execute the function to perform analysis
    analyze_this()
