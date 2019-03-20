"""Implement a pure python binary search tree"""

from pyds.BinarySearchTree import BinarySearchTreeNode, BinarySearchTree


class SimpleBinarySearchTreeNode(BinarySearchTreeNode):
    """Implement an AVL compatible node."""

    def __init__(self, key):
        """Constructor."""
        super().__init__(key)

    def update(self):
        """No need for update in a simple node."""
        pass


class SimpleBinarySearchTree(BinarySearchTree):
    """Implement an AVL BST."""

    def __init__(self):
        """Constructor."""
        super().__init__()

    def _rebalance(self, node):
        """Provide placeholder for AVL."""
        pass

    def insert(self, node):
        """Insert a node in the tree."""
        # Call BST insert first
        super().insert(node)
        if self._root is None:
            self._root = node
        else:
            self._root._insert(node)
        self._rebalance(node)

    def delete(self, key):
        """Delete a node from the tree."""
        # Call BST delete first
        super().delete(key)
        # Implement delete operation
        node = self.find(key)
        deleted = None
        if not key == node.key:
            return deleted
        if node is self._root:
            pseudoroot = SimpleBinarySearchTreeNode(None)
            pseudoroot.left = self._root
            self._root.parent = pseudoroot
            deleted = self._root._delete()
            self._root = pseudoroot.left
            if self._root is not None:
                self._root.parent = None
        else:
            deleted = node._delete()
        self._rebalance(deleted.parent)
        deleted.parent = None
        return deleted

    def _merge_at_root(self, lnode, rnode, root):
        """Merge two node to a common root."""
        root.left = lnode
        if lnode is not None:
            lnode.parent = root
        root.right = rnode
        if rnode is not None:
            rnode.parent = root
        root.update()
        return root

    def _fast_merge_trees(self, ltree, rtree):
        """Merge avl separated and larger rtree to ltree."""
        root = ltree._root.max()
        ltree.delete(root.key)
        ltree._root = self._merge_at_root(
            ltree._root, rtree.root, root
        )
        rtree._root = None

    def _slow_merge_trees(self, ltree, rtree):
        """Merge slow but all type of trees."""
        node = rtree.min()
        while node is not None:
            key = node.key
            node = rtree.delete(key)
            ltree.insert(node)
            node = rtree.min()

    def merge(self, tree):
        """Merge tree to self."""
        if self._root is None or tree._root is None:
            return
        rootmax = self._root.max()
        rootmin = self._root.min()
        treemax = tree.max()
        treemin = tree.min()
        if rootmax.key < treemin.key:
            self._fast_merge_trees(self, tree)
        elif treemax.key < rootmin.key:
            self._fast_merge_trees(tree, self)
            self._root = tree._root
            tree._root = None
        else:
            self._slow_merge_trees(self, tree)

    def _split(self, root, key):
        """Split a tree from key."""
        if root == None:
            return None, None
        if key < root.key:
            lnode, mnode = self._split(root.left, key)
            rnode = self._merge_at_root(mnode, root.right, root)
            return lnode, rnode
        mnode, rnode = self._split(root.right, key)
        lnode = self._merge_at_root(root.left, mnode, root)
        return lnode, rnode

    def split(self, key):
        """Split self returning right side."""
        nodetype = type(self)
        rtree = nodetype()
        if self._root is None:
            return rtree
        self._root, rnode = self._split(self._root, key)
        rtree._root = rnode
        return rtree
