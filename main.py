
class Leaf:
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


# Example usage:
if __name__ == "__main__":
    # Create a sample tree
    root = Leaf(1, 10)
    child1 = Leaf(1, 4)
    child2 = Leaf(2, 4)
    child3 = Leaf(5, 8)
    
    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)
    
    # Find best match for interval (2,3)
    best_match = root.find_best_match(2, 3)
    print(f"Best match for interval (2,3): {best_match}")
    
    # Test parent-child relationships
    print(f"Parent of best match: {best_match.parent}")
    print(f"Root's children: {root.children}")
    
    # Test common ancestor
    common = child1.find_common_ancestor(child2)
    print(f"Common ancestor of {child1} and {child2}: {common}")
