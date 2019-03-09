from pyds.DisjointSet import DisjointSet
import pytest

import random
import sys
import uuid


def test_disjoint_set_initialization():
    """Test disjoint set initialization."""
    ds = DisjointSet(range(10))
    for i in range(10):
        assert ds.find(i) == i
        assert ds.size(i) == 1


def test_disjoint_set_union():
    """Test disjoint set union."""
    ds = DisjointSet(range(10))
    ds.union(3,4)
    assert ds.find(3) == ds.find(4)
    assert ds.size(3) == ds.size(4)
    assert ds.size(3) == 2
    assert ds.size(4) == 2
    ds.union(5,6)
    assert ds.find(5) == ds.find(6)
    assert ds.size(5) == ds.size(6)
    assert ds.size(5) == 2
    assert ds.size(6) == 2
    ds.union(3,6)
    assert ds.find(3) == ds.find(5)
    assert ds.find(4) == ds.find(6)
    assert ds.size(3) == ds.size(5)
    assert ds.size(4) == ds.size(6)
    assert ds.size(3) == 4
    assert ds.size(5) == 4
