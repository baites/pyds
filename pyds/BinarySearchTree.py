"""Implement a pure python binary search tree"""

import abc


class BinarySearchTreeNode(abc.ABC):
    """Implement a base class for a tree node."""

    def __init__(self, key):
        """Constructor."""
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.nodelabel = lambda node: str(node.key)

    def _str(self):
        """Internal method for ASCII art."""
        label = self.nodelabel(self)
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
        node = self
        while 1:
            if key == node.key:
                break
            elif key < node.key:
                if node.left is not None:
                    node = node.left
                else:
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    break
        return node

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

    def _insert(self, node):
        """Inserts a node into the subtree rooted at this node."""
        parent = self.find(node.key)
        if node.key == parent.key:
            return
        if node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
        node.parent = parent

    def _delete(self):
        """Deletes and returns this node from subtree rooted at this node."""
        node = self
        while 1:
            if node.left is None or node.right is None:
                if node is node.parent.left:
                    node.parent.left = node.left or node.right
                    if node.parent.left is not None:
                        node.parent.left.parent = node.parent
                else:
                    node.parent.right = node.left or node.right
                    if node.parent.right is not None:
                        node.parent.right.parent = node.parent
                node.left = None
                node.right = None
                break
            else:
                next = node.next()
                node.key, next.key = next.key, node.key
                node = next
        return node


class BinarySearchTree(abc.ABC):
    """Implement a base class for binary trees."""

    def __init__(self):
        """Constructor."""
        self._root = None

    def __str__(self):
        """Print the tree."""
        if self._root is None:
            return '<empty tree>'
        return str(self._root)

    def find(self, key):
        """Finds and returns the node with given key."""
        return self._root and self._root.find(key)

    def next(self, key):
        """Returns the node that contains the next larger key."""
        node = self.find(key)
        return node and node.next()

    def min(self):
        """Returns the minimum node in the tree."""
        return self._root and self._root.min()

    def max(self):
        """Returns the minimum node in the tree."""
        return self._root and self._root.max()

    @abc.abstractmethod
    def insert(self, node):
        """Define insert API."""
        pass

    @abc.abstractmethod
    def delete(self, key):
        """Define insert API."""
        return self

    @abc.abstractmethod
    def merge(self, tree):
        """Merge tree to self."""
        pass

    #@abc.abstractmethod
    #def split(self, key):
    #    """Split self returning right side."""
    #    return self

    @property
    def root(self):
        """Return root as read-only property."""
        return self._root
