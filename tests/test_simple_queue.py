from pyds.SimpleQueue import SimpleQueue
from pyds.exception import EmptyList
import pytest

import random
import sys
import uuid


queue_size = 100


def test_empty_queue():
    """Test empty queue behavior."""
    q = SimpleQueue()
    assert len(q) == 0
    with pytest.raises(EmptyList):
        q.dequeue()


def test_simple_queue():
    """Test queue enqueue and dequeue behavior."""
    q = SimpleQueue()
    inputs = []
    for i in range(queue_size):
        value = str(uuid.uuid4())
        inputs.append(value)
        q.enqueue(value)
    assert q.peek() == inputs[0]
    index = 0
    while len(q) > 0:
        assert q.dequeue() == inputs[index]
        index += 1
