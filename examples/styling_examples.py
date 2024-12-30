"""Examples demonstrating styling capabilities."""

from tree_interval import Leaf, LeafStyle, Position


def test_styling():
    """Test basic styling functionality."""
    node = Leaf(Position(0, 100), info="Test")
    style = LeafStyle(color="#FF0000", bold=True)
    node.style = style
    assert node.style.color == "#FF0000"
    assert node.style.bold is True


def run_demo():
    print("=== Rich Styling Examples ===")
    test_styling()


if __name__ == "__main__":
    run_demo()
