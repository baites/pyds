
from pyds.SimpleBinarySearchTree import SimpleBinarySearchTreeNode
from pyds.SimpleBinarySearchTree import SimpleBinarySearchTree
from pyds.IntervalTree import Interval, IntervalTreeNode
from pyds.IntervalTree import IntervalTree
import random


def main():
    """Main example."""
    # Define the tree type
    Tree = IntervalTree(
        treetype=SimpleBinarySearchTree
    )

    # Define actual tree instance
    tree = Tree()

    # Define intervals
    intervals = [
        (0,3), (5,8), (6,10), (8,9), (15,23),
        (16,21), (17,19), (19,20), (25,30), (26,26)
    ]
    random.shuffle(intervals)

    # Define the node to be inserted
    Node = IntervalTreeNode(
        nodetype=SimpleBinarySearchTreeNode
    )

    # Insert the nodes
    for low, high in intervals:
        tree.insert(
            Node(Interval(low, high))
        )

    # Print original tree
    print('Initial interval tree:')
    print(tree)
    print()

    # Look for intervals
    node = tree.interval(Interval(18,19))
    print(node.key.low, node.key.high)

if __name__ == "__main__":
    main()
