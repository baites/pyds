"""Implement a pure python binary search tree"""

from pyds.BinarySearchTree import BinarySearchTreeNode, BinarySearchTree


class AVLBinarySearchTreeNode(BinarySearchTreeNode):
    """Implement an AVL compatible node."""

    def __init__(self, key):
        """Constructor."""
        super().__init__(key)
        self._height = 0

    def update(self):
        """Update the height after rebalancing."""
        left = self.left._height if self.left is not None else -1
        right = self.right._height if self.right is not None else -1
        self._height = max(left, right) + 1

    @property
    def height(self):
        return self._height


class AVLBinarySearchTree(BinarySearchTree):
    """Implement an AVL BST."""

    def __init__(self):
        """Constructor."""
        super().__init__()

    @staticmethod
    def _height(node):
        return node._height if node is not None else -1

    def _left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self._root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.right = y.left
        if x.right is not None:
            x.right.parent = x
        y.left = x
        x.parent = y
        x.update()
        y.update()

    def _right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self._root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.left = y.right
        if x.left is not None:
            x.left.parent = x
        y.right = x
        x.parent = y
        x.update()
        y.update()

    def _rebalance(self, node):
        while node is not None:
            node.update()
            if self._height(node.left) >= 2 + self._height(node.right):
                if self._height(node.left.left) >= self._height(node.left.right):
                    self._right_rotate(node)
                else:
                    self._left_rotate(node.left)
                    self._right_rotate(node)
            elif self._height(node.right) >= 2 + self._height(node.left):
                if self._height(node.right.right) >= self._height(node.right.left):
                    self._left_rotate(node)
                else:
                    self._right_rotate(node.right)
                    self._left_rotate(node)
            node = node.parent

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
            pseudoroot = AVLBinarySearchTreeNode(None)
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
        if abs(lnode.height - rnode.height) <= 1:
            root.left = lnode
            root.right = rnode
            lnode.parent = root
            rnode.parent = root
            root.update()
            return root
        elif lnode.height > rnode.height:
            root = cls._merge_at_root(
                lnode.right, rnode, root
            )
            lnode.right = root
            root.parent = lnode
            self._rebalance(lnode)
            return lnode
        elif lnode.height < rnode.height:
            root = cls._merge_at_root(
                lnode, rnode.left, root
            )
            rnode.left = root
            root.parent = rnode
            self._rebalance(rnode)
            return rnode

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
