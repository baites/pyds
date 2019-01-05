"""Implement a pure python SinglyLinkedList."""

from collections.abc import Sized, Iterator, Iterable
from pyds.exception import EmptyList


class SinglyLinkedNode:
    """Implement a double linked node."""

    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedListIter(Iterator):
    """Implement a list iterator."""
    def __init__(self, node):
        """Constructor."""
        self._node = node
        self._stop_iter = False

    def __next__(self):
        """Return the next item in the list."""
        if self._stop_iter:
            raise StopIteration
        if not self._node:
            self._stop_iter = True
            raise StopIteration
        value = self._node.value
        self._node = self._node.next
        return value


class SinglyLinkedList(Sized, Iterable):
    """Implement the actual list."""
    def __init__(self):
        """Constructor."""
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        """Return list size."""
        return self._size

    def __iter__(self):
        """Return a list iterator."""
        return SinglyLinkedListIter(self._head)

    def push_front(self, value):
        """Push value in the front of the list O(1)."""
        node = SinglyLinkedNode(value)
        node.next = self._head
        self._head = node
        self._size += 1
        if not self._tail:
            self._tail = self._head

    def pop_front(self):
        """Pop value from the front of the list O(1)."""
        if not self._head:
            raise EmptyList('Cannot pop front value.')
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        node.next = None
        self._size -= 1
        return node.value

    def front(self):
        """Return value at the front of the list O(1)."""
        if not self._head:
            raise EmptyList('Cannot return front value.')
        return self._head.value

    def back(self):
        """Return value at the back of the list O(1)."""
        if not self._tail:
            raise EmptyList('Cannot return back value.')
        return self._tail.value
