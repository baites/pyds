"""Implement a pure python binary search tree"""

from pyds.SimpleBinarySearchTree import SimpleBinarySearchTreeNode
from pyds.SimpleBinarySearchTree import SimpleBinarySearchTree


class AVLBinarySearchTreeNode(SimpleBinarySearchTreeNode):
    """Implement an AVL compatible node."""

    def __init__(self, key):
        """Constructor."""
        super().__init__(key)
        self._height = 0
        self.nodelabel = lambda node: str(
            '{},{}'.format(node.key, node._height)
        )

    def update(self):
        """Update the height after rebalancing."""
        left = self.left._height if self.left is not None else -1
        right = self.right._height if self.right is not None else -1
        self._height = max(left, right) + 1

    @property
    def height(self):
        return self._height


class AVLBinarySearchTree(SimpleBinarySearchTree):
    """Implement an AVL BST."""

    def __init__(self, root=None):
        """Constructor."""
        super().__init__(root)


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

    def _temp(self, node, n=100):
        if node is None:
            print(None)
            return
        counter = 0
        print()
        print(node)
        pnode = node.parent
        while counter < n and node.parent is not None:
            node = node.parent
            counter += 1
        if counter < n:
            print('---')
        else:
            print()
            print(pnode)
            print('***')
            raise ValueError()


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

    def _avl_merge_at_root(self, lnode, rnode, pnode):
        """Merge two node to a common root."""
        # Simplest case, direct merging
        if lnode is None or rnode is None or\
            abs(lnode.height - rnode.height) <= 1:
            return self._merge_at_root(lnode, rnode, pnode)

        # Search for insertion point to keep balanced
        knode = None
        while abs(lnode.height - rnode.height) > 1:
            if lnode.height > rnode.height:
                knode = lnode
                lnode = lnode.right
            else:
                knode = rnode
                rnode = rnode.left

        # Merge pnode into insertion point
        pnode = self._merge_at_root(lnode, rnode, pnode)
        if knode.right is lnode:
            knode.right = pnode
            pnode.parent = knode
            self._rebalance(pnode)
        else:
            knode.left = pnode
            pnode.parent = knode
            self._rebalance(pnode)

        # Locate new root
        while knode.parent is not None:
            knode = knode.parent

        return knode

    def _fast_merge_trees(self, ltree, rtree):
        """Merge avl separated and larger rtree to ltree."""
        root = ltree._root.max()
        root = ltree.delete(root.key)
        ltree._root = self._avl_merge_at_root(
            ltree._root, rtree._root, root
        )
        rtree._root = None

    def _disconnect(self, node):
        pnode = node.parent
        node.parent = None
        if pnode is not None:
            if node is pnode.right:
                pnode.right = None
            else:
                pnode.left = None
            self._rebalance(pnode)
        lnode = node.left
        if lnode is not None:
            lnode.parent = None
            node.left = None
        rnode = node.right
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
