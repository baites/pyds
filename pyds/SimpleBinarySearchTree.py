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

    def __init__(self, root=None):
        """Constructor."""
        super().__init__(root)

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
        # Getting self type
        treetype = type(self._root)
        # Implement delete operation
        node = self.find(key)
        deleted = None
        if not key == node.key:
            return deleted
        if node is self._root:
            pseudoroot = treetype(None)
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
        root.parent = None
        root.update()
        return root

    def _fast_tree_merger(self, ltree, rtree):
        """Merge separated with rtree containing largest values."""
        root = ltree._root.max()
        root = ltree.delete(root.key)
        ltree._root = self._merge_at_root(
            ltree._root, rtree._root, root
        )
        rtree._root = None

    def _slow_tree_merger(self, ltree, rtree):
        """Merge slow but all type of trees."""
        node = rtree.min()
        while node is not None:
            key = node.key
            node = rtree.delete(key)
            ltree.insert(node)
            node = rtree.min()

    def merge(self, tree):
        """Merge tree to self."""
        # Check empty tree
        if tree._root is None:
            return
        # Check for empty self
        if self._root is None:
            self._root = tree._root
            tree._root = None
            return

        # Check if tree has one node and just insert
        if tree._root.left is None and\
            tree._root.right is None:
            self.insert(tree._root)
            tree._root = None
            return
        # Check if self has one node and just insert
        if self._root.left is None and\
            self._root.right is None:
            tree.insert(self._root)
            self._root = tree._root
            tree._root = None
            return

        # Check for tree separation
        rootmax = self._root.max()
        rootmin = self._root.min()
        treemax = tree.max()
        treemin = tree.min()

        # Merge trees
        if rootmax.key < treemin.key:
            self._fast_tree_merger(self, tree)
        elif treemax.key < rootmin.key:
            self._fast_tree_merger(tree, self)
            self._root = tree._root
            tree._root = None
        else:
            self._slow_tree_merger(self, tree)

    def _disconnect(self, node):
        """Disconect a node from its parent and child."""
        # Diconnect from parent
        pnode = node.parent
        node.parent = None
        if pnode is not None:
            if node is pnode.right:
                pnode.right = None
            else:
                pnode.left = None
            pnode.update()

        # Diconnect from left child
        lnode = node.left
        if lnode is not None:
            lnode.parent = None
            node.left = None
        rnode = node.right

        # Diconnect from right child
        if rnode is not None:
            rnode.parent = None
            node.right = None
        node.update()
        return lnode, pnode, rnode

    def split(self, key):
        """Split a tree in two trees."""

        # Define tree types
        treetype = type(self)
        ltree = treetype()
        rtree = treetype()

        # Find key node
        node = self._root.find(key)
        lnode, pnode, rnode = self._disconnect(node)
        ltree.merge(treetype(lnode))
        rtree.merge(treetype(rnode))
        if node.key < key or node.key == key:
            ltree.insert(node)
        else:
            rtree.insert(node)
        node = pnode

        # Iterative mergers
        while node is not None:
            lnode, pnode, rnode = self._disconnect(node)
            if key < node.key:
                rtree.merge(treetype(rnode))
                rtree.insert(node)
            else:
                ltree.merge(treetype(lnode))
                ltree.insert(node)
            node = pnode

        self._root = ltree._root
        return rtree
