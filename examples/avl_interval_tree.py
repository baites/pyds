
from pyds.AVLBinarySearchTree import AVLBinarySearchTreeNode
from pyds.AVLBinarySearchTree import AVLBinarySearchTree
import random


class Interval:
    """Implement interval use as key."""

    def __init__(self, low, high):
        """Constructor."""
        self.low = low
        self.high = high

    def __eq__(self, other):
        return self.low == other.low and\
                self.high == self.high

    def __lt__(self, other):
        return self.low < other.low


class Node(AVLBinarySearchTreeNode):
    """Implement avl node for implementing an interval tree."""

    def __init__(self, low, high):
        """Constructor."""
        super().__init__(
            Interval(low, high)
        )
        self.maxhigh = high

    def label(self):
        """Customize node label."""
        return '[{},{}]|{}'.format(self.key.low, self.key.high, self.maxhigh)

    def update(self):
        """Customize node update the keysum."""
        # Call parent update first
        super().update()
        self.maxhigh = self.key.high
        if self.left is not None:
            self.maxhigh = max(self.maxhigh, self.left.maxhigh)
        if self.right is not None:
            self.maxhigh = max(self.maxhigh, self.right.maxhigh)

    def overlap(self, interval):
        """Check if interval overlap with self."""
        if self.key.high < interval.low or interval.high < self.key.low:
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
                and node.left.maxhigh >= interval.low:
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
    node = tree.interval(Interval(18,19))
    print(node.key.low, node.key.high)

if __name__ == "__main__":
    main()
