from collections.abc import Sized
from pyds.DoublyLinkedList import DoublyLinkedList
from pyds.exception import EmptyQueue

class SimpleQueue(Sized):
    """Implement a sinple queue by adapting a DoublyLinkedList."""

    def __init__(self):
        """Constructor."""
        self._list = DoublyLinkedList()
        self._list._empty_list = EmptyQueue

    def __len__(self):
        """Return list size."""
        return len(self._list)

    def enqueue(self, value):
        """Enqueue an item in the queue."""
        self._list.push_front(value)

    def dequeue(self):
        """Dequeue an item from the queue."""
        return self._list.pop_back()

    def peek(self):
        """Peek at the first element to dequeue."""
        return self._list.back()
