
from pyds.AVLBinarySearchTree import AVLBinarySearchTreeNode
from pyds.AVLBinarySearchTree import AVLBinarySearchTree


class Node(AVLBinarySearchTreeNode):
    """Implement avl node that show height per node."""
    def __init__(self, key):
        super().__init__(key)
        self.leftsize = 0
        self.rightsize = 0

    def label(self):
        """Cutomize node label."""
        return '{},{},{}'.format(self.leftsize, self.key, self.rightsize)

    def update(self):
        """Customize node update the keysum."""
        # Call parent update first
        super().update()
        self.leftsize = 0
        if self.left is not None:
            self.leftsize = self.left.leftsize + self.left.rightsize + 1
        self.rightsize = 0
        if self.right is not None:
            self.rightsize = self.right.leftsize + self.right.rightsize + 1


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

    print('Split original tree into left and right trees')
    rtree = ltree.split(36)
    print()

    print('Left tree:')
    print(ltree)
    print()
    print('Right tree:')
    print(rtree)
    print()

    # Merge the trees
    print('Merge rtree into ltree')
    ltree.merge(rtree)
    print()

    # Print output
    print('Left tree:')
    print(ltree)
    print()

    print('Right tree:')
    print(rtree)
    print()


if __name__ == "__main__":
    main()
