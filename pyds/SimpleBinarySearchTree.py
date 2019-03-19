"""Implement a pure python binary search tree"""

from pyds.BinarySearchTree import BinarySearchTreeNode, BinarySearchTree


class SimpleBinarySearchTreeNode(BinarySearchTreeNode):
    """Implement a simple tree node."""
    def __init__(self, key):
        """Constructor."""
        super().__init__(key)

    def update(self):
        """No need for update in a simple node."""
        pass


class SimpleBinarySearchTree(BinarySearchTree):
    """Implement a simple BST."""

    def __init__(self, nodetype=SimpleBinarySearchTreeNode):
        """Constructor."""
        super().__init__(nodetype)

    def insert(self, key, *args, **kwargs):
        """Insert a node in the tree."""
        # Call BST insert first
        super().insert(key, *args, **kwargs)
        # Implement insert operation
        node = self.nodetype(key, *args, **kwargs)
        if self.root is None:
            self.root = node
        else:
            self.root._insert(node)

    def delete(self, key):
        """Delete a node from the tree."""
        # Call BST delete first
        super().delete(key)
        # Implement delete operation
        node = self.find(key)
        deleted = None
        if not key == node.key:
            return deleted
        if node is self.root:
            pseudoroot = BinarySearchTreeNode(None)
            pseudoroot.left = self.root
            self.root.parent = pseudoroot
            deleted = self.root._delete()
            self.root = pseudoroot.left
            if self.root is not None:
                self.root.parent = None
        else:
            deleted = node._delete()
        return deleted

    @staticmethod
    def _merge_at_root(node1, node2, root):
        root.left = node1
        root.right = node2
        node1.parent = root
        node2.parent = root
        root.update()
        return root

    @classmethod
    def _fast_merge_trees(cls, ltree, rtree):
        """Merge fast for separated trees."""
        root = ltree.root.max()
        ltree.delete(root.key)
        ltree.root = cls._merge_at_root(
            ltree.root, rtree.root, root
        )
        rtree.root = None

    @classmethod
    def _slow_merge_trees(cls, ltree, rtree):
        """Merge slow for non separated trees."""
        node = rtree.min()
        while node is not None:
            key = node.key
            rtree.delete(key)
            ltree.insert(key)
            node = rtree.min()

    def merge(self, tree):
        """Merge tree to self."""
        if self.root is None or tree.root is None:
            return
        rootmax = self.root.max()
        treemin = tree.min()
        if rootmax.key < treemin.key:
            self._fast_merge_trees(self, tree)
        else:
            self._slow_merge_trees(self, tree)
