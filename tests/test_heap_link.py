import pytest
from src.fibonacci_heap import FibonacciHeap, Node

def test_heap_link_basic():
    """Test if the heap links two nodes correctly"""
    # make two nodes
    heap = FibonacciHeap()
    x = Node(1)
    y = Node(10)
    heap._root_add(x)
    heap._root_add(y)
    x.degree = 0
    y.degree = 0
    
    # Both are in root list before link
    roots_before = [node.key for node in heap._iterate_list(x)]
    assert 1 in roots_before and 10 in roots_before

    heap._heap_link(y, x)
    
    # y should now be a child of x
    assert y.parent is x
    assert x.child is not None
    assert x.degree == 1
    assert y.mark is False

    # y should not be in the root list anymore
    roots_after = [node.key for node in heap._iterate_list(x)]
    assert 10 not in roots_after  # only 1 is in root list nowpy