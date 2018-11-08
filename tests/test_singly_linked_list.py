from pyds.SinglyLinkedList import SinglyLinkedList
from pyds.exception import EmptyList
import pytest


items = [i for i in range(5)]


def test_empty_list():
    """Test empty list behavior."""
    l = SinglyLinkedList()
    assert len(l) == 0
    with pytest.raises(EmptyList):
        l.front()


def test_front_methods():
    """Test front methods."""
    l = SinglyLinkedList()

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
