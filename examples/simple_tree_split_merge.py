
from pyds.SimpleBinarySearchTree import SimpleBinarySearchTreeNode
from pyds.SimpleBinarySearchTree import SimpleBinarySearchTree


def main():
    """Main example."""
    # Create the trees
    ltree = SimpleBinarySearchTree()
    rtree = SimpleBinarySearchTree()

    # Populate original tree
    for i in range(1,41):
        ltree.insert(SimpleBinarySearchTreeNode(i))

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
