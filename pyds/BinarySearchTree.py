"""Implement a pure python binary search tree"""

import abc


class TreeNode(abc.ABC):
    """Implement a base class for a tree node."""

    def __init__(self, key):
        """Constructor."""
        self.key = key
        self.parent = None
        self.left = None
        self.right = None

    def _str(self):
        """Internal method for ASCII art."""
        label = str(self.key)
        if self.left is None:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = self.left._str()
        if self.right is None:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = self.right._str()
        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)
        if (middle - len(label)) % 2 == 1 and self.parent is not None and \
           self is self.parent.left and len(label) < middle:
            label += '.'
        label = label.center(middle, '.')
        if label[0] == '.': label = ' ' + label[1:]
        if label[-1] == '.': label = label[:-1] + ' '
        lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle-2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
          [left_line + ' ' * (width - left_width - right_width) + right_line
           for left_line, right_line in zip(left_lines, right_lines)]
        return lines, pos, width

    def __str__(self):
        return '\n'.join(self._str()[0])

    abc.abstractmethod
    def update(self):
        """Provide place holder for update function."""
        pass

    def find(self, key):
        """Find node with given key."""
        if key == self.key:
            return self
        elif key < self.key:
            if self.left is not None:
                return self.left.find(key)
            return self
        else:
            if self.right is not None:
                return self.right.find(key)
            return self

    def min(self):
        """Return the node min key."""
        node = self
        while node.left is not None:
            node = node.left
        return node

    def max(self):
        """Return the node max key."""
        node = self
        while node.right is not None:
            node = node.right
        return node

    def next(self):
        """Find the node in the tree with the next largest key."""
        if self.right is not None:
            return self.right.min()
        node = self
        while node.parent is not None and node is node.parent.right:
            node = node.parent
        return node.parent

    def insert(self, node):
        """Inserts a node into the subtree rooted at this node."""
        if node is None:
            return
        if node.key < self.key:
            if self.left is None:
                node.parent = self
                self.left = node
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                node.parent = self
                self.right = node
            else:
                self.right.insert(node)

    def delete(self):
        """Deletes and returns this node from the tree."""
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right is not None:
                    self.parent.right.parent = self.parent
            return self
        else:
            next = self.next()
            self.key, next.key = next.key, self.key
            return next.delete()


class BinarySeachTree(abc.ABC):
    """Implement a base class for binary trees."""

    def __init__(self, nodetype):
        """Constructor."""
        self.root = None
        self.nodetype = nodetype

    def __str__(self):
        """Print the tree."""
        if self.root is None:
            return '<empty tree>'
        return str(self.root)

    def find(self, key):
        """Finds and returns the node with given key."""
        return self.root and self.root.find(key)

    def next(self, key):
        """Returns the node that contains the next larger key."""
        node = self.find(key)
        return node and node.next()

    def min(self):
        """Returns the minimum node in the tree."""
        return self.root and self.root.min()

    def max(self):
        """Returns the minimum node in the tree."""
        return self.root and self.root.max()

    @abc.abstractmethod
    def insert(self, key):
        """Define insert API."""
        pass

    @abc.abstractmethod
    def delete(self, key):
        """Define insert API."""
        pass


class SimpleTreeNode(TreeNode):
    """Implement a simple tree node."""
    def __init__(self, key):
        """Constructor."""
        super().__init__(key)

    def update(self):
        """No need for update in a simple node."""
        pass


class SimpleBinarySearchTree(BinarySeachTree):
    """Implement a simple BST."""

    def __init__(self, nodetype=SimpleTreeNode):
        """Constructor."""
        super().__init__(nodetype)

    def insert(self, key, *args, **kwargs):
        """Insert a node in the tree."""
        node = self.nodetype(key, *args, **kwargs)
        if self.root is None:
            self.root = node
        else:
            self.root.insert(node)

    def delete(self, key):
        """Delete a node from the tree."""
        node = self.find(key)
        if node is None:
            return None
        if node is self.root:
            pseudoroot = TreeNode(None)
            pseudoroot.left = self.root
            self.root.parent = pseudoroot
            deleted = self.root.delete()
            self.root = pseudoroot.left
            if self.root is not None:
                self.root.parent = None
        else:
            deleted = node.delete()


class AVLTreeNode(TreeNode):
    """Implement an avl compatible node."""

    def __init__(self, key):
        """Constructor."""
        super().__init__(key)
        self.heigh = None

    def update(self):
        """Update the height after rebalancing."""
        left = self.left.height if self.left is not None else -1
        right = self.right.height if self.right is not None else -1
        self.height = max(left, right) + 1


class AVLBinarySearchTree(BinarySeachTree):
    """Implement an AVL BST."""

    def __init__(self, nodetype=AVLTreeNode):
        """Constructor."""
        super().__init__(nodetype)

    @staticmethod
    def _height(node):
        return node.height if node is not None else -1

    def _left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
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
            self.root = y
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

    def insert(self, key, *args, **kwargs):
        """Insert a node in the tree."""
        node = self.nodetype(key, *args, **kwargs)
        if self.root is None:
            self.root = node
        else:
            self.root.insert(node)
        self._rebalance(node)

    def delete(self, key):
        """Delete a node from the tree."""
        node = self.find(key)
        if node is None:
            return None
        if node is self.root:
            pseudoroot = AVLTreeNode(None)
            pseudoroot.left = self.root
            self.root.parent = pseudoroot
            deleted = self.root.delete()
            self.root = pseudoroot.left
            if self.root is not None:
                self.root.parent = None
        else:
            deleted = node.delete()
        self._rebalance(deleted.parent)

    @staticmethod
    def _merge_at_root(node1, node2, root):
        """Merge two node to a common root."""
        if abs(node1.height - node2.height) <= 1:
            root.left = node1
            root.right = node2
            node1.parent = root
            node2.parent = root
            root.height = max(
                node1.height, node2.height
            ) + 1
            return root
        elif node1.height > node2.height:
            temp = self._merge_at_root(
                node1.right, node2, root
            )
            node1.right = temp
            temp.parent = node1
            self._rebalance(node1)
            return root
        elif node1.height < node2.height:
            temp = self._merge_at_root(
                node1, node2.right, root
            )
            node2.right = temp
            temp.parent = node2
            self._rebalance(node2)
            return root

    @staticmethod
    def _merge_at_root2(node1, node2, root):
        root.left = node1
        root.right = node2
        node1.parent = root
        node2.parent = root
        root.height = max(
            node1.height, node2.height
        ) + 1
        return root


    def merge(self, tree):
        """Merge avl tree to self."""
        root = self.root.max()
        root = root.delete()
        self.root = self._merge_at_root(
            self.root, tree.root, root
        )


import random

#tree = SimpleBinarySearchTree()
tree1 = AVLBinarySearchTree()
tree2 = AVLBinarySearchTree()

for i in range(9):
    #tree1.insert(random.randint(1,200))
    tree1.insert(i)
print(tree1)
print()
for i in range(9,14):
    #tree2.insert(random.randint(1,200))
    tree2.insert(i)
print(tree2)
print()

tree1.merge(tree2)
print(tree1)
