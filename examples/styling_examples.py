
"""Examples demonstrating styling capabilities."""

from rich.style import Style as RichStyle
from tree_interval import Leaf, Position, Tree, LeafStyle


def test_styling():
    """Test basic styling functionality."""
    node = Leaf(Position(0, 100), info="Test")
    style = LeafStyle(color="#FF0000", bold=True)
    node.style = style
    assert node.style.color == "#FF0000"
    assert node.style.bold is True


if __name__ == "__main__":
    test_styling()

