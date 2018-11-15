from pyds.PriorityQueue import PriorityQueue
from pyds.exception import EmptyQueue
import pytest

import random
import sys
import uuid


maxpriority = 1000
queue_size = 100
stress_iterations = 10


def test_empty_queue():
    """Test empty queue behavior."""
    q = PriorityQueue()
    assert len(q) == 0
    with pytest.raises(EmptyQueue):
        q.dequeue()


def test_priority_queue():
    """Test queue enqueue and dequeue behavior."""
    q = PriorityQueue()
    for iteration in range(stress_iterations):
        inputs = []
        for i in range(queue_size):
            priority = random.randint(0, maxpriority)
            inputs.append(priority)
            q.enqueue(priority, str(uuid.uuid4()))
        prioritys = []
        while len(q) > 0:
            priority, value, _ = q.dequeue()
            prioritys.append(priority)
        for i in range(1, len(prioritys)):
            assert prioritys[i] >= prioritys[i-1]


def test_priority_update():
    """Test queue priority change."""
    q = PriorityQueue()

    for iteration in range(stress_iterations):
        inputs = []
        for i in range(queue_size):
            priority = random.randint(1, maxpriority)
            inputs.append(priority)
            q.enqueue(priority, str(uuid.uuid4()))

        test = q._heap[random.randint(0,len(q._heap)-1)]
        q.enqueue(0, test.value)

        priority, value, _ = q.dequeue()
        assert test.value == value
