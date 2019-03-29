"""Implement a pure python interval tree
   where tree implementation is specified by policy.
"""


class Interval:
    """Implement interval use as key."""

    def __init__(self, low, high):
        """Constructor."""
        self.low = low
        self.high = high

    def __eq__(self, other):
        return self.low == other.low

    def __lt__(self, other):
        return self.low < other.low


def IntervalTreeNode(nodetype):
    """Create node for an interval tree."""

    class _(nodetype):
        """Implement node for an interval tree."""

        def __init__(self, interval):
            """Constructor."""
            super().__init__(interval)
            self.maxhigh = interval.high

        def label(self):
            """Customize node label."""
            return '[{},{}]|{}'.format(
                self.key.low, self.key.high, self.maxhigh
            )

        def update(self):
            """Customize node update the keysum."""
            # Call parent update first
            super().update()
            self.maxhigh = self.key.high
            if self.left is not None:
                self.maxhigh = max(self.maxhigh, self.left.maxhigh)
            if self.right is not None:
                self.maxhigh = max(self.maxhigh, self.right.maxhigh)

        def overlap(self, interval):
            """Check if interval overlap with self."""
            if self.key.high < interval.low or interval.high < self.key.low:
                return False
            return True

    return _


def IntervalTree(treetype):
    """Create an interval tree."""

    class _(treetype):
        """Create an interval tree."""

        def __init__(self, root=None):
            """Constructor."""
            super().__init__(root)

        def interval(self, interval):
            """Return a node that overlap with point."""
            node = self._root
            while node is not None and\
                not node.overlap(interval):
                if node.left is not None \
                    and node.left.maxhigh >= interval.low:
                    node = node.left
                else:
                    node = node.right
            return node

    return _
