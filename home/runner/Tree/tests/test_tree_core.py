import unittest
from tree import Node

class TestTreeCore(unittest.TestCase):
    def test_find_parent(self):
        root = Node(info={"type": "Module"})
        child1 = Node(info={"type": "FunctionDef"}, parent=root)
        grandchild = Node(info={"type": "Return"}, parent=child1)

        found = grandchild.find_parent(lambda n: n.info and n.info.get("type") == "FunctionDef")
        self.assertEqual(found, child1)

        found = grandchild.find_parent(lambda n: n.info and n.info.get("type") == "Module")
        self.assertEqual(found, root)

        found = root.find_parent(lambda n: n.info and n.info.get("type") == "Module")
        self.assertIsNone(found)


    def test_find_child(self):
        root = Node(info={"type": "Module"})
        child1 = Node(info={"type": "Assign"}, parent=root)
        child2 = Node(info={"type": "FunctionDef"}, parent=root)

        found = root.find_child(lambda n: n.info and n.info.get("type") == "Assign")
        self.assertEqual(found, child1)

        found = root.find_child(lambda n: n.info and n.info.get("type") == "FunctionDef")
        self.assertEqual(found, child2)

        found = child1.find_child(lambda n: n.info and n.info.get("type") == "Assign")
        self.assertIsNone(found)


    def test_find_sibling(self):
        root = Node(info={"type": "Module"})
        child1 = Node(info={"type": "Assign"}, parent=root)
        child2 = Node(info={"type": "FunctionDef"}, parent=root)

        found = child1.find_sibling(lambda n: n.info and n.info.get("type") == "FunctionDef")
        self.assertEqual(found, child2)

        found = child2.find_sibling(lambda n: n.info and n.info.get("type") == "Assign")
        self.assertEqual(found, child1)

        found = root.find_sibling(lambda n: n.info and n.info.get("type") == "Assign")
        self.assertIsNone(found)

    def test_find_parent_no_info(self):
        root = Node()
        child1 = Node(parent=root)
        grandchild = Node(parent=child1)

        found = grandchild.find_parent(lambda n: n.info and n.info.get("type") == "FunctionDef")
        self.assertIsNone(found)

    def test_find_child_no_info(self):
        root = Node()
        child1 = Node(parent=root)
        child2 = Node(parent=root)

        found = root.find_child(lambda n: n.info and n.info.get("type") == "Assign")
        self.assertIsNone(found)


    def test_find_sibling_no_info(self):
        root = Node()
        child1 = Node(parent=root)
        child2 = Node(parent=root)

        found = child1.find_sibling(lambda n: n.info and n.info.get("type") == "FunctionDef")
        self.assertIsNone(found)

if __name__ == '__main__':
    unittest.main()