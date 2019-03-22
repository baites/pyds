
from pyds.SimpleBinarySearchTree import SimpleBinarySearchTreeNode
from pyds.SimpleBinarySearchTree import SimpleBinarySearchTree
import random


tree_inserts = 100
tree_deletes = tree_inserts//2
tree_ops = 30
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


def assert_deleted_node(node):
    """Assert condition for a deleted node."""
    assert node.parent is None
    assert node.left is None
    assert node.right is None


def test_insert():
    """Test insert operation."""
    # Create the tree
    tree = SimpleBinarySearchTree()
    # Populate tree with insert
    keys = set()
    for i in range(tree_inserts):
        key = random.randint(min_key, max_key)
        keys.add(key)
        tree.insert(SimpleBinarySearchTreeNode(key))
    # Assert basic tree conditions
    assert_search_binary_tree_invariance(keys, tree)


def test_delete():
    """Test delete operation."""
    # Create the tree
    tree = SimpleBinarySearchTree()
    # Populate tree with insert
    keys = set()
    for i in range(tree_inserts):
        key = random.randint(min_key, max_key)
        keys.add(key)
        tree.insert(SimpleBinarySearchTreeNode(key))
    # Assert tree invariances after multiple deletions
    for n in range(tree_inserts-1, tree_deletes-1, -1):
        # Delete one node
        key = random.sample(keys, k=1)[0]
        keys -= set([key])
        node = tree.delete(key)
        assert key == node.key
        assert_deleted_node(node)
        assert_search_binary_tree_invariance(keys, tree)


def test_fast_merge_separated_bigger_right():
    """Test fast merge separated tree bigger on the right."""
    # Populate trees
    for i in range(tree_ops):
        # Create tree to be merge
        ltree = SimpleBinarySearchTree()
        keys = set()
        for i in range(tree_inserts):
            key = random.randint(
                min_key, (max_key-min_key)//2+min_key
            )
            keys.add(key)
            ltree.insert(SimpleBinarySearchTreeNode(key))
        rtree = SimpleBinarySearchTree()
        for i in range(tree_inserts):
            key = random.randint(
                (max_key-min_key)//2+min_key+1, max_key
            )
            keys.add(key)
            rtree.insert(SimpleBinarySearchTreeNode(key))
        ltree.merge(rtree)
        assert_search_binary_tree_invariance(keys, ltree)


def test_fast_merge_separated_bigger_left():
    """Test slow merge separated tree bigger on the left."""
    # Populate trees
    for i in range(tree_ops):
        # Create tree to be merge
        ltree = SimpleBinarySearchTree()
        keys = set()
        for i in range(tree_inserts):
            key = random.randint(
                (max_key-min_key)//2+min_key+1, max_key
            )
            keys.add(key)
            ltree.insert(SimpleBinarySearchTreeNode(key))
        rtree = SimpleBinarySearchTree()
        for i in range(tree_inserts):
            key = random.randint(
                min_key, (max_key-min_key)//2+min_key
            )
            keys.add(key)
            rtree.insert(SimpleBinarySearchTreeNode(key))
        ltree.merge(rtree)
        assert_search_binary_tree_invariance(keys, ltree)


def test_slow_merge_overlapped_trees():
    """Test slow merge for overlapping trees."""
    # Populate trees
    for i in range(tree_ops):
        # Create tree to be merge
        ltree = SimpleBinarySearchTree()
        keys = set()
        for i in range(tree_inserts):
            key = random.randint(min_key, max_key)
            keys.add(key)
            ltree.insert(SimpleBinarySearchTreeNode(key))
        rtree = SimpleBinarySearchTree()
        for i in range(tree_inserts):
            key = random.randint(min_key, max_key)
            keys.add(key)
            rtree.insert(SimpleBinarySearchTreeNode(key))
        ltree.merge(rtree)
        assert_search_binary_tree_invariance(keys, ltree)


def test_split_tree():
    """Test tree splitting."""
    for i in range(tree_ops):
        # Create the tree
        ltree = SimpleBinarySearchTree()
        # Populate tree with insert
        keys = set()
        for i in range(tree_inserts):
            key = random.randint(min_key, max_key)
            keys.add(key)
            ltree.insert(SimpleBinarySearchTreeNode(key))
        skey = random.sample(keys, k=1)[0]
        rtree = ltree.split(skey)
        lkeys = set()
        rkeys = set()
        for key in keys:
            if key <= skey:
                lkeys.add(key)
            else:
                rkeys.add(key)
        # Check invariances for ltree
        assert_search_binary_tree_invariance(lkeys, ltree)
        # Check invariances for rtree
        assert_search_binary_tree_invariance(rkeys, rtree)
        # Merge the tree
        ltree.merge(rtree)
        # Check invariance of merged tree
        assert_search_binary_tree_invariance(lkeys | rkeys, ltree)
