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

    def _merge_at_root(self, lnode, rnode, root):
        """Merge two node to a common root."""
        if lnode is None or rnode is None:
            root.left = lnode
            if lnode is not None:
                lnode.parent = root
            root.right = rnode
            if rnode is not None:
                rnode.parent = root
            root.update()
            return root
        elif abs(lnode.height - rnode.height) <= 1:
            root.left = lnode
            root.right = rnode
            lnode.parent = root
            rnode.parent = root
            root.update()
            return root
        elif lnode.height > rnode.height:
            root = self._merge_at_root(
                lnode.right, rnode, root
            )
            lnode.right = root
            root.parent = lnode
            self._rebalance(lnode)
            return lnode
        elif lnode.height < rnode.height:
            root = self._merge_at_root(
                lnode, rnode.left, root
            )
            rnode.left = root
            root.parent = rnode
            self._rebalance(rnode)
            return rnode
