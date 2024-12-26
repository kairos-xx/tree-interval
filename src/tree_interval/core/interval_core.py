# src/tree_interval/__init__.py
from .core.interval_core import Tree, Leaf, Position
from .visualizer import VisualizationConfig
from .builder import AstIntervalBuilder


# src/tree_interval/core/interval_core.py
class Tree:
    pass

class Leaf:
    pass

class Position:
    pass

# src/tree_interval/visualizer.py
class VisualizationConfig:
    pass

# src/tree_interval/builder.py
class AstIntervalBuilder:
    pass


# main.py
from src.tree_interval import Tree, Leaf, Position, VisualizationConfig, AstIntervalBuilder

# Example usage
tree = Tree()
leaf = Leaf()
position = Position()
config = VisualizationConfig()
builder = AstIntervalBuilder()

print("Example program ran successfully.")