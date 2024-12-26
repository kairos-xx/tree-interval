
class Tree:
    def __init__(self):
        self.root = None
    
    def add_leaf(self, new_leaf):
        if not isinstance(new_leaf, Leaf):
            raise TypeError("Must be a Leaf instance")
            
        if not self.root:
            self.root = new_leaf
            return
            
        best_parent = new_leaf.find_best_parent(self.root)
        if best_parent:
            best_parent.add_child(new_leaf)
        else:
            raise ValueError("Cannot find suitable parent for the new leaf")
            
    def find_best_match(self, target_start: int, target_end: int) -> 'Leaf':
        if not self.root:
            return None
        return self.root.find_best_match(target_start, target_end)
        
    def add_leaves(self, leaves):
        if not leaves:
            return
            
        # Sort leaves by interval size (largest first) and start position
        sorted_leaves = sorted(leaves, key=lambda x: (-(x.end - x.start), x.start))
        
        self.root = sorted_leaves[0]
        for leaf in sorted_leaves[1:]:
            self.add_leaf(leaf)


class Leaf:
    @classmethod
    def from_list(cls, leaves):
        if not leaves:
            return None
            
        # Sort leaves by interval size (largest first) and start position
        sorted_leaves = sorted(leaves, key=lambda x: (-(x.end - x.start), x.start))
        
        root = sorted_leaves[0]
        for leaf in sorted_leaves[1:]:
            current = root
            placed = False
            
            while not placed:
                # Check if it's a sibling
                if leaf.start == current.start and leaf.end == current.end:
                    current.add_sibling(leaf)
                    placed = True
                    continue
                
                # Find appropriate child position
                if current.start <= leaf.start and leaf.end <= current.end:
                    # Check existing children first
                    child_placed = False
                    for child in current.children:
                        if child.start <= leaf.start and leaf.end <= child.end:
                            current = child
                            child_placed = True
                            break
                    
                    if not child_placed:
                        current.add_child(leaf)
                        placed = True
                else:
                    raise ValueError(f"Interval {leaf} cannot be placed in the tree")
                    
        return root

    def __init__(self, start: int, end: int, info=None):
        if start > end:
            raise ValueError("Start must be less than or equal to end")
        self.start = start
        self.end = end
        self.info = info
        self.children = []
        self.parent = None
        self.siblings = []

    def add_child(self, child):
        if not isinstance(child, Leaf):
            raise TypeError("Child must be a Leaf instance")
        
        # Check if it's actually a sibling
        if child.start == self.start and child.end == self.end:
            self.add_sibling(child)
            return
            
        # Validate interval containment
        if not (self.start <= child.start and child.end <= self.end):
            raise ValueError("Child interval must be contained within parent interval")
            
        # Check if any existing children should become children of the new leaf
        children_to_move = []
        for existing_child in self.children:
            if (child.start <= existing_child.start and 
                existing_child.end <= child.end):
                children_to_move.append(existing_child)
        
        # Remove children that will be moved
        for move_child in children_to_move:
            self.children.remove(move_child)
            child.children.append(move_child)
            move_child.parent = child
            
        child.parent = self
        self.children.append(child)
        
    def add_sibling(self, sibling):
        if not isinstance(sibling, Leaf):
            raise TypeError("Sibling must be a Leaf instance")
        if sibling.start != self.start or sibling.end != self.end:
            raise ValueError("Siblings must have the same interval")
        if sibling not in self.siblings:
            self.siblings.append(sibling)
            sibling.siblings.append(self)

    def find_best_match(self, target_start: int, target_end: int) -> 'Leaf':
        def calculate_distance(leaf):
            start_diff = abs(leaf.start - target_start)
            end_diff = abs(leaf.end - target_end)
            return start_diff + end_diff

        best_leaf = self
        min_distance = calculate_distance(self)

        # Check current node's children
        for child in self.children:
            if (child.start <= target_start and child.end >= target_end):
                child_best = child.find_best_match(target_start, target_end)
                child_distance = calculate_distance(child_best)
                if child_distance < min_distance:
                    best_leaf = child_best
                    min_distance = child_distance

        return best_leaf

    def find_common_ancestor(self, other: 'Leaf') -> 'Leaf':
        if not isinstance(other, Leaf):
            raise TypeError("Argument must be a Leaf instance")
            
        # Get path to root for both leaves
        path1 = self._path_to_root()
        path2 = other._path_to_root()
        
        # Find first common ancestor
        for node in path1:
            if node in path2:
                return node
                
        return None

    def _path_to_root(self):
        path = [self]
        current = self
        while current.parent is not None:
            path.append(current.parent)
            current = current.parent
        return path

    def __repr__(self):
        return f"Leaf({self.start}, {self.end}, info={self.info})"
        
    def find_best_parent(self, root):
        if not root:
            return None
            
        if root.start > self.start or root.end < self.end:
            return None
            
        best_parent = root
        for child in root.children:
            if (child.start <= self.start and self.end <= child.end):
                potential_parent = self.find_best_parent(child)
                if potential_parent:
                    best_parent = potential_parent
                    
        return best_parent
        
    @classmethod
    def add_to_tree(cls, root, new_leaf):
        if not root:
            return new_leaf
            
        best_parent = new_leaf.find_best_parent(root)
        if best_parent:
            best_parent.add_child(new_leaf)
        else:
            raise ValueError("Cannot find suitable parent for the new leaf")
            
        return root


# Example usage:
if __name__ == "__main__":
    # Create leaves
    leaf1 = Leaf(1, 4)
    leaf2 = Leaf(2, 4)
    leaf3 = Leaf(5, 8)
    root = Leaf(1, 10)
    
    # Create tree and add leaves
    tree = Tree()
    tree.add_leaves([root, leaf1, leaf2, leaf3])
    
    # Find best match for interval (2,3)
    best_match = root.find_best_match(2, 3)
    print(f"Best match for interval (2,3): {best_match}")
    
    # Test parent-child relationships
    print(f"Parent of best match: {best_match.parent}")
    print(f"Root's children: {root.children}")
    
    # Test common ancestor
    common = leaf1.find_common_ancestor(leaf2)
    print(f"Common ancestor of {leaf1} and {leaf2}: {common}")
