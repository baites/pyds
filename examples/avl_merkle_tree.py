
from pyds.AVLBinarySearchTree import AVLBinarySearchTreeNode
from pyds.AVLBinarySearchTree import AVLBinarySearchTree


class Node(AVLBinarySearchTreeNode):
    """Implement avl node that show height per node."""
    module = 1000

    def __init__(self, key):
        super().__init__(key)
        self.lhash = 0
        self.rhash = 0

    def label(self):
        """Customize node label."""
        return '{},{},{}'.format(self.lhash, self.key, self.rhash)

    def update(self):
        """Customize node update the keysum."""
        # Call parent update first
        super().update()
        self.lhash = 0
        self.rhash = 0
        if self.left is not None:
            self.lhash = self.left.key.__hash__()
            self.lhash = (self.lhash + self.left.lhash + self.left.rhash) % self.module
        if self.right is not None:
            self.rhash = self.right.key.__hash__()
            self.rhash = (self.rhash + self.right.lhash + self.right.rhash) % self.module

def main():
    """Main example."""
    # Create the trees
    tree = AVLBinarySearchTree()

    # Words
    words = """
        this was the biggest disappointment of our trip. the restaurant had received some very good reviews, so our expectations were high.
        the service was slow even though the restaurant was not very full.
    """

    # Mercle tree
    for word in words.split():
        tree.insert(Node(word.strip()))

    # Print original tree
    print('Initial mercle tree:')
    print(tree)
    print()


if __name__ == "__main__":
    main()
