
from pyds.AVLBinarySearchTree import AVLBinarySearchTreeNode
from pyds.AVLBinarySearchTree import AVLBinarySearchTree
import random


tree_inserts = 100
tree_deletes = tree_inserts//2
tree_merges = 30
min_key = 1
max_key = 100
stress_iterations = 10


def assert_search_binary_tree_invariance(keys, tree):
    """Assert binary search condition."""
    for key in keys:
        node = tree.find(key)
        assert key == node.key
        if node.parent is not None:
            assert not node.key == node.parent.key
            if node is node.parent.left:
                assert node.key < node.parent.key
            elif node is node.parent.right:
                assert not node.key < node.parent.key
        if node.left is not None:
            assert node.left.key < node.key
        if node.right is not None:
            assert not node.right.key == node.key
            assert not node.right.key < node.key


def assert_avl_invariance(keys, tree):
    """Assert AVL search binary tree condition."""
    for key in keys:
        node = tree.find(key)
        left = node.left.height if node.left is not None else 0
        right = node.right.height if node.right is not None else 0
        assert abs(left - right) <= 1


def assert_deleted_node(node):
    """Assert condition for a deleted node."""
    assert node.parent is None
    assert node.left is None
    assert node.right is None


def test_insert():
    """Test insert operation."""
    # Create the tree
    tree = AVLBinarySearchTree()
    # Populate tree with insert
    keys = set()
    for i in range(tree_inserts):
        key = random.randint(min_key, max_key)
        keys.add(key)
        tree.insert(AVLBinarySearchTreeNode(key))
    # Assert basic tree conditions
    assert_search_binary_tree_invariance(keys, tree)
    assert_avl_invariance(keys, tree)


def test_delete():
    """Test delete operation."""
    # Create the tree
    tree = AVLBinarySearchTree()
    # Populate tree with insert
    keys = set()
    for i in range(tree_inserts):
        key = random.randint(min_key, max_key)
        keys.add(key)
        tree.insert(AVLBinarySearchTreeNode(key))
    # Assert tree invariances after multiple deletions
    for n in range(tree_inserts-1, tree_deletes-1, -1):
        # Delete one node
        key = random.sample(keys, k=1)[0]
        keys -= set([key])
        node = tree.delete(key)
        assert key == node.key
        assert_deleted_node(node)
        assert_search_binary_tree_invariance(keys, tree)
        assert_avl_invariance(keys, tree)
