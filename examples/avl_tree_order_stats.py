
from pyds.AVLBinarySearchTree import AVLBinarySearchTreeNode
from pyds.AVLBinarySearchTree import AVLBinarySearchTree


class Node(AVLBinarySearchTreeNode):
    """Implement avl node that show height per node."""
    def __init__(self, key):
        super().__init__(key)
        self.keysum = 0

    def label(self):
        """Customize node label."""
        return '{},{}'.format(self.key, self.keysum)

    def update(self):
        """Customize node update the keysum."""
        # Call parent update first
        super().update()
        leftsum = 0 if self.left is None else self.left.keysum
        rightsum = 0 if self.right is None else self.right.keysum
        self.keysum = self.key + leftsum + rightsum


def main():
    """Main example."""
    # Create the trees
    ltree = AVLBinarySearchTree()
    rtree = AVLBinarySearchTree()

    # Populate original tree
    for i in range(1,41):
        ltree.insert(Node(i))

    # Print original tree
    print('Original tree:')
    print(ltree)
    print()

    print('Split original tree for key = 36')
    rtree = ltree.split(36)
    print()

    print('Left tree:')
    print(ltree)
    print()

    print('The root of the left tree should be (36+37)/2 = 666')
    print()

    # Merge the trees
    print('Split original left tree for key = 33')
    rtree = ltree.split(33)
    print()

    # Print output
    print('Right tree:')
    print(rtree)
    print()

    print('The root of the right tree should be 34+35+36 = 105')
    print()

if __name__ == "__main__":
    main()
