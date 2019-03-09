"""Implement a pure python DisjointSet."""


class DisjointSetNode:
    """Implement a disjoint set node."""

    def __init__(self, key):
        """Constructor."""
        self.parent = key
        self.size = 1


class DisjointSet:
    """Implement a disjoin set."""

    def __init__(self, iterable=[]):
        """Constructor."""
        self._node = {
            key: DisjointSetNode(key) for key in iterable
        }

    def add(self, key):
        """Add a new set with one key."""
        self._node[key] = DisjointSetNode(key)

    def find(self, key):
        """Find parent key of a given key."""
        if key != self._node[key].parent:
            self._node[key].parent = self.find(self._node[key].parent)
        return self._node[key].parent

    def size(self, key):
        """Get the size of a set."""
        kid = self.find(key)
        return self._node[kid].size

    def union(self, x, y):
        """Union two set given any of their keys."""
        xid = self.find(x)
        yid = self.find(y)
        if xid == yid:
            return
        if self._node[xid].size < self._node[yid].size:
            self._node[xid].parent = yid
            self._node[yid].size += self._node[xid].size
        else:
            self._node[yid].parent = xid
            self._node[xid].size += self._node[xid].size
