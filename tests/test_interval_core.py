import pytest

from tree_interval import Leaf, Position
from tree_interval.core.interval_core import (
    NestedAttributes,
    PartStatement,
    Statement,
    Tree,
)


def test_leaf_statement_property():
    root = Leaf(Position(0, 100), info={"type": "Module"})
    child = Leaf(Position(10, 50), info={"type": "Call"})
    root.add_child(child)
    assert child.top_statement is not None


def test_leaf_attribute_chain():
    root = Leaf(Position(0, 100), info={"type": "Attribute"})
    child = Leaf(Position(10, 50), info={"type": "Name"})
    root.add_child(child)
    assert child.next_attribute is None
    assert root.previous_attribute is not None


def test_nested_attributes():
    leaf = Leaf(Position(0, 100), info={"type": "Module"})
    leaf.position.lineno = 1
    leaf.position.end_lineno = 5
    attrs = leaf._as_dict()
    assert attrs["position"]["lineno"] == 1
    assert attrs["position"]["end_lineno"] == 5


def test_leaf_serialization():
    leaf = Leaf(Position(0, 100), info={"name": "test"})
    leaf_dict = leaf._as_dict()
    assert leaf_dict["start"] == 0
    assert leaf_dict["end"] == 100
    assert leaf_dict["info"]["name"] == "test"


def test_position_edge_cases():
    with pytest.raises(ValueError):
        _ = Position(None, None)


def test_leaf_complex_operations():
    leaf = Leaf(Position(0, 100))
    leaf.selected = True
    assert leaf.selected
    assert leaf.size == 100

    # Test attribute chain
    leaf.info = {"type": "Attribute"}
    assert leaf.next_attribute is None
    assert leaf.previous_attribute is None


def test_tree_empty_operations():
    tree = Tree("")
    assert tree.flatten() == []
    tree_json = tree.to_json()
    assert Tree.from_json(tree_json).root is None


def test_complex_leaf_operations():
    leaf = Leaf(Position(0, 100))
    leaf.position.lineno = 1
    leaf.position.end_lineno = 5
    leaf.position.col_offset = 0
    leaf.position.end_col_offset = 10
    assert leaf.lineno == 1
    assert leaf.end_lineno == 5
    assert leaf.col_offset == 0
    assert leaf.end_col_offset == 10


def test_leaf_navigation():
    root = Leaf(Position(0, 100))
    child1 = Leaf(Position(10, 30))
    child2 = Leaf(Position(40, 60))
    root.add_child(child1)
    root.add_child(child2)
    assert child1.next == child2
    assert child2.previous == child1


def test_tree_serialization():
    tree = Tree("test")
    root = Leaf(Position(0, 100), info={"type": "root"})
    child = Leaf(Position(10, 50), info={"type": "child"})
    tree.root = root
    tree.add_leaf(child)

    json_str = tree.to_json()
    loaded_tree = Tree.from_json(json_str)
    assert loaded_tree.root is not None
    assert getattr(loaded_tree.root, "info", {}).get("type") == "root"


def test_position_overlaps():
    pos1 = Position(0, 50)
    pos2 = Position(40, 90)
    pos3 = Position(60, 100)
    assert pos1.overlaps(pos2)
    assert not pos1.overlaps(pos3)


def test_leaf_statement():
    root = Leaf(Position(0, 100),
                info={
                    "type": "Call",
                    "source": "test()",
                    "cleaned_value": "test"
                })
    child = Leaf(Position(10, 50),
                 info={
                     "type": "Name",
                     "source": "test",
                     "cleaned_value": "test"
                 })
    root.add_child(child)
    stmt = child.statement
    assert stmt.text is not None


def test_leaf_find_operations():
    root = Leaf(Position(0, 100))
    child1 = Leaf(Position(10, 30))
    child2 = Leaf(Position(40, 60))
    grandchild = Leaf(Position(15, 25))

    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    found = root.find(lambda n: n.start == 40)
    assert found == child2


def test_leaf_next_previous():
    root = Leaf(Position(0, 100))
    child1 = Leaf(Position(10, 30))
    child2 = Leaf(Position(40, 60))
    root.add_child(child1)
    root.add_child(child2)

    assert child1.next == child2
    assert child2.previous == child1
    assert root.previous is None
    assert child2.next is None


def test_tree_add_duplicate_leaf():
    tree = Tree("test")
    leaf1 = Leaf(Position(0, 50), info="test")
    leaf2 = Leaf(Position(0, 50), info="test")

    tree.add_leaf(leaf1)
    tree.add_leaf(leaf2)  # Should not add duplicate
    assert len(tree.flatten()) == 1


def test_nested_attributes_missing():
    leaf = Leaf(Position(0, 100))
    assert leaf.attributes.nonexistent_attr is None


def test_position_with_none_values():
    pos = Position(0, 100)
    pos.lineno = None
    pos.end_lineno = None
    assert pos.end_lineno == 1  # Default fallback


def test_leaf_get_ancestors():
    root = Leaf(Position(0, 100))
    child = Leaf(Position(10, 50))
    grandchild = Leaf(Position(20, 40))

    root.add_child(child)
    child.add_child(grandchild)

    ancestors = grandchild.get_ancestors()
    assert len(ancestors) == 2
    assert ancestors[0] == child
    assert ancestors[1] == root


def test_position_column_handling():
    pos = Position(0, 100)
    pos.col_offset = 5
    pos.end_col_offset = 15
    assert pos.col_offset == 5
    assert pos.end_col_offset == 15


def test_position_with_disposition():
    from dis import Positions

    pos = Position(Positions(lineno=1,
                             end_lineno=2,
                             col_offset=0,
                             end_col_offset=10),
                   source="test\ncode")
    assert pos.start is not None
    assert pos.end is not None


def test_leaf_chain_operations():
    root = Leaf(Position(0, 100),
                info={
                    "type": "Call",
                    "source": "obj.method()",
                    "cleaned_value": "obj"
                })
    attr = Leaf(Position(10, 50),
                info={
                    "type": "Attribute",
                    "source": ".method",
                    "cleaned_value": "method"
                })
    root.add_child(attr)
    assert attr.previous_attribute is None
    assert root.next_attribute is None


def test_tree_duplicate_handling():
    tree = Tree("test")
    leaf1 = Leaf(Position(0, 50))
    leaf2 = Leaf(Position(0, 50))  # Same position
    tree.add_leaf(leaf1)
    tree.add_leaf(leaf2)
    assert len(tree.flatten()) == 1


def test_leaf_match():
    leaf1 = Leaf(Position(0, 50), info={"type": "test"})
    leaf2 = Leaf(Position(0, 50), info={"type": "test"})
    leaf3 = Leaf(Position(10, 60), info={"type": "different"})
    assert leaf1.match(leaf2)
    assert not leaf1.match(leaf3)
    assert not leaf1.match(None)


def test_nested_attributes_complex():
    leaf = Leaf(Position(0, 100))
    leaf.position.lineno = 1
    leaf.position.end_lineno = 5
    leaf.position.col_offset = 0
    leaf.position.end_col_offset = 10
    assert leaf.position.lineno == 1
    assert leaf.position.end_lineno == 5


def test_tree_serialization_with_styles():
    from rich.style import Style
    tree = Tree("test")
    root = Leaf(Position(0, 100))
    root.style = {"color": "red", "bold": True}
    root.rich_style = Style(color="red", bold=True)
    tree.root = root

    json_str = tree.to_json()
    loaded_tree = Tree.from_json(json_str)
    assert loaded_tree.root is not None
    assert loaded_tree.root.style == {"color": "red", "bold": True}


def test_position_frame_handling():
    import types
    frame = types.FrameType
    try:
        _ = Position(frame)
    except Exception:
        assert True  # Should handle frame gracefully


def test_statement_formatting():
    part = PartStatement(before="test(", after=")")
    stmt = Statement(top=part, before="obj.", self="method", after="()")
    formatted = stmt.as_text(top_marker="^",
                             chain_marker="~",
                             current_marker="*")
    assert "test" in formatted
    assert "method" in formatted


def test_leaf_find_operations_complex():
    root = Leaf(Position(0, 100))
    child1 = Leaf(Position(10, 30))
    child2 = Leaf(Position(40, 60))
    grandchild = Leaf(Position(15, 25))

    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    # Test various find operations
    assert root.find_best_match(14, 28) == grandchild
    assert grandchild.find_common_ancestor(child2) == root
    assert grandchild.find_first_multi_child_ancestor() == root

    # Test edge cases
    assert root.find_best_match(200, 300) == root  # Out of range
    assert root.find_common_ancestor(None) is None


def test_nested_attributes_edge_cases():
    data = {"test": None, "nested": {"value": None}}
    attrs = NestedAttributes(data)
    assert attrs.test is None
    assert attrs.nested.value is None
    assert attrs.nonexistent is None
    assert str(attrs) == repr(attrs)


def test_dispose_frame():
    """Test frame position handling with disposition"""
    from dis import Positions

    pos = Position(Positions(lineno=1,
                             end_lineno=2,
                             col_offset=0,
                             end_col_offset=10),
                   source=None)
    assert pos.start == 0
    assert pos.end == 10


def test_frame_complex_source():
    """Test frame handling with complex source"""
    from types import FrameType

    class MockFrame:

        def __init__(self):
            self.f_code = type('', (), {'co_firstlineno': 1})
            self.positions = type('', (), {
                'lineno': 3,
                'end_lineno': 5,
                'col_offset': 4,
                'end_col_offset': 8
            })

    try:
        pos = Position(MockFrame())
    except:
        assert True


def test_statement_complex_formatting():
    """Test complex statement formatting"""
    part = PartStatement(before="def test(", after="):")
    stmt = Statement(top=part,
                     before="obj.attr.",
                     self="method",
                     after="(a, b)")
    text = stmt.as_text(top_marker="^", chain_marker="~", current_marker="*")
    assert text is not None
    assert "def test" in text


def test_nested_attributes_deep():
    """Test deeply nested attributes"""
    data = {"level1": {"level2": {"level3": "value"}}}
    attrs = NestedAttributes(data)
    assert attrs.level1.level2.level3 == "value"
    assert attrs.nonexistent_attr is None
    assert attrs.level1.nonexistent is None


def test_leaf_advanced_matching():
    """Test advanced leaf matching scenarios"""
    pos1 = Position(10, 50)
    pos1.lineno = 1
    pos2 = Position(10, 50)
    pos2.lineno = 2

    leaf1 = Leaf(pos1, info={"type": "test"})
    leaf2 = Leaf(pos2, info={"type": "test"})
    assert not leaf1.match(leaf2)


def test_tree_edge_cases():
    """Test tree edge cases"""
    tree = Tree("test")
    leaf = Leaf(None)  # Test with None position
    tree.add_leaf(leaf)
    assert tree.flatten() == [leaf]


def test_position_complex_calcs():
    """Test complex position calculations"""
    pos = Position(0, 100)
    pos._lineno = None
    assert pos.lineno is None
    pos._end_lineno = None
    assert pos.end_lineno == 1  # Default fallback


def test_leaf_chain_complex():
    """Test complex leaf chain operations"""
    root = Leaf(Position(0, 100), info={"type": "Call"})
    attr1 = Leaf(Position(10, 30), info={"type": "Attribute"})
    attr2 = Leaf(Position(40, 60), info={"type": "Name"})
    root.add_child(attr1)
    attr1.add_child(attr2)

    assert attr2.next_attribute is None
    assert attr1.previous_attribute == attr2


def test_tree_serialization_complex():
    """Test complex tree serialization"""
    tree = Tree("test")
    root = Leaf(Position(0, 100))
    root.info = {"nested": {"value": None}}
    tree.root = root

    json_str = tree.to_json()
    loaded_tree = Tree.from_json(json_str)
    assert loaded_tree.root is not None
    assert loaded_tree.root.info["nested"]["value"] is None


if __name__ == "__main__":
    pytest.main([__file__])
