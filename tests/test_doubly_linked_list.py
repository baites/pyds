from pyds.DoublyLinkedList import DoublyLinkedList
from pyds.exception import EmptyList
import pytest


items = [i for i in range(5)]


def test_empty_list():
    """Test empty list behavior."""
    l = DoublyLinkedList()
    assert len(l) == 0
    with pytest.raises(EmptyList):
        l.front()
    with pytest.raises(EmptyList):
        l.back()


def test_front_methods():
    """Test front methods."""
    l = DoublyLinkedList()

    # Test push_front method and front.
    counter = 1
    for item in items:
        l.push_front(item)
        assert l.front() == item
        assert len(l) == counter
        counter += 1

    # Test list iterator
    index = len(items) - 1
    for value in l:
        assert value == items[index]
        index -= 1

    # Test pop_front method
    for item in reversed(items):
        value = l.pop_front()
        assert value == item


def test_back_methods():
    """Test front methods."""
    l = DoublyLinkedList()

    # Test push_front method and front.
    counter = 1
    for item in items:
        l.push_back(item)
        assert l.back() == item
        assert len(l) == counter
        counter += 1

    # Test list iterator
    index = len(items) - 1
    for value in reversed(l):
        assert value == items[index]
        index -= 1

    # Test pop_front method
    for item in reversed(items):
        value = l.pop_back()
        assert value == item
