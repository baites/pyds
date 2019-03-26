
from pyds.AVLBinarySearchTree import AVLBinarySearchTreeNode
from pyds.AVLBinarySearchTree import AVLBinarySearchTree
import random


class Node(AVLBinarySearchTreeNode):
    """Implement avl node for implementing an interval tree."""

    def __init__(self, key, high):
        super().__init__(key)
        self.high = high
        self.max = max

    def label(self):
        """Customize node label."""
        return '[{},{}]|{}'.format(self.key, self.high, self.max)

    def update(self):
        """Customize node update the keysum."""
        # Call parent update first
        super().update()
        self.max = self.high
        if self.left is not None:
            self.max = max(self.max, self.left.max)
        if self.right is not None:
            self.max = max(self.max, self.right.max)

    def overlap(self, interval):
        """Check if interval overlap with self."""
        if self.high < interval.key or interval.high < self.key:
            return False
        return True


class IntervalTree(AVLBinarySearchTree):
    """Implement interval tree based on AVL."""

    def __init__(self, root=None):
        """Constructor."""
        super().__init__(root)

    def interval(self, interval):
        """Return a node that overlap with point."""
        node = self._root
        while node is not None \
            and not node.overlap(interval):
            if node.left is not None \
                and node.left.max >= interval.key:
                node = node.left
            else:
                node = node.right
        return node


def main():
    """Main example."""
    # Create the trees
    tree = IntervalTree()

    intervals = [
        (0,3), (5,8), (6,10), (8,9), (15,23),
        (16,21), (17,19), (19,20), (25,30), (26,26)
    ]

    random.shuffle(intervals)

    for low, high in intervals:
        tree.insert(Node(low, high))

    # Print original tree
    print('Initial interval tree:')
    print(tree)
    print()

    # Look for intervals
    node = tree.interval(Node(18,19))
    print(node.key, node.high)

if __name__ == "__main__":
    main()
