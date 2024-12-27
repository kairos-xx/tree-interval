
import unittest
from src.tree_interval import Tree, Leaf, Position
 
class TestTreeCore(unittest.TestCase):
    def test_find_parent(self):
        root = Leaf(Position(0, 100, {"type": "Module"}))
        child1 = Leaf(Position(10, 50, {"type": "FunctionDef"}))
        grandchild = Leaf(Position(20, 40, {"type": "Return"}))

        root.add_child(child1)
        child1.add_child(grandchild)

        found = grandchild.find_parent(lambda n: bool(n.info and n.info.get("type") == "FunctionDef"))
        self.assertEqual(found, child1)

        found = grandchild.find_parent(lambda n: bool(n.info and n.info.get("type") == "Module"))
        self.assertEqual(found, root)

        found = root.find_parent(lambda n: bool(n.info and n.info.get("type") == "Module"))
        self.assertIsNone(found)

    def test_find_child(self):
        root = Leaf(Position(0, 100, {"type": "Module"}))
        child1 = Leaf(Position(10, 40, {"type": "Assign"}))
        child2 = Leaf(Position(50, 90, {"type": "FunctionDef"}))

        root.add_child(child1)
        root.add_child(child2)

        found = root.find_child(lambda n: bool(n.info and n.info.get("type") == "Assign"))
        self.assertEqual(found, child1)

        found = root.find_child(lambda n: bool(n.info and n.info.get("type") == "FunctionDef"))
        self.assertEqual(found, child2)

        found = child1.find_child(lambda n: bool(n.info and n.info.get("type") == "Assign"))
        self.assertIsNone(found)

    def test_find_sibling(self):
        root = Leaf(Position(0, 100, {"type": "Module"}))
        child1 = Leaf(Position(10, 40, {"type": "Assign"}))
        child2 = Leaf(Position(50, 90, {"type": "FunctionDef"}))

        root.add_child(child1)
        root.add_child(child2)

        found = child1.find_sibling(lambda n: bool(n.info and n.info.get("type") == "FunctionDef"))
        self.assertEqual(found, child2)

if __name__ == "__main__":
    unittest.main()
