"""Implement a pure python priority queue"""

from collections.abc import Container, Sized
from pyds.exception import EmptyQueue


class Item:
    """Implement an queue item."""
    def __init__(self, priority, value, key):
        self.priority = priority
        self.value = value
        self.key = key

    """Sorting criteria."""
    def __lt__(self, item):
        return self.priority < item.priority


class PriorityQueue(Container, Sized):
    """Implement an queue item."""
    def __init__(self):
        """Constructor."""
        self._heap = []
        self._index = {}
        self._size = 0

    def __contains__(self, key):
        """Check if a key is in the container."""
        return key in self._index

    def __len__(self):
        """Return lenght of the queue."""
        return self._size

    def _swap(self, i, j):
        """Swap to elements of the heap."""
        tmp = self._heap[i]
        self._heap[i] = self._heap[j]
        self._index[self._heap[j].key] = i
        self._heap[j] = tmp
        self._index[tmp.key] = j

    def _sift_up(self, i):
        """Sift up an element in the heap."""
        while i > 0:
            p = (i-1)//2
            if self._heap[i] < self._heap[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def _sift_down(self, i):
        """Sift down an element in the heap."""
        mini = i
        l = 2*i + 1
        if l < self._size and\
            self._heap[l] < self._heap[mini]:
            mini = l
        r = 2*i + 2
        if r < self._size and\
            self._heap[r] < self._heap[mini]:
            mini = r
        if mini != i:
            self._swap(i, mini)
            self._sift_down(mini)

    def _update(self, priority, key):
        """Update an element in the heap."""
        i = self._index[key]
        item = self._heap[i]
        old_priority = item.priority
        item.priority = priority
        if priority < old_priority:
            self._sift_up(i)
        else:
            self._sift_down(i)

    def enqueue(self, priority, value, key=None):
        """Enqueue an item in the queue."""
        key = key if key else value
        if key in self._index:
            self._update(priority, key)
            return
        self._heap.append(Item(priority, value, key))
        self._size = len(self._heap)
        self._index[key] = self._size - 1
        self._sift_up(self._size - 1)

    def dequeue(self):
        """Dequeue an item from the queue."""
        if self._size == 0:
            raise EmptyQueue('dequeue from empty queue')
        priority = self._heap[0].priority
        value = self._heap[0].value
        key = self._heap[0].key
        del self._index[key]
        item = self._heap.pop()
        self._size -= 1
        if self._size == 0:
            return priority, value, key
        self._heap[0] = item
        self._index[item.key] = 0
        self._sift_down(0)
        return priority, value, key

    def peek(self):
        """Peek at the first element to dequeue."""
        if self._size == 0:
            raise EmptyQueue('pop from empty queue')
        priority = self._heap[0].priority
        value = self._heap[0].value
        key = self._heap[0].key
        return priority, value, key
