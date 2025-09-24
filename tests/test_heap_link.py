from src.fibonacci_heap import FibonacciHeap, Node
import pytest

def test_heap_link_basic():
    """test if the heap link correctly adds two nodes together"""
    heap = FibonacciHeap()
    x = Node(1)
    y = Node(10)

    # ad nodes to root list
    heap._root_add(x)
    heap._root_add(y)

    # The nodes should be in root list and have no parent or children
    assert x.parent is None
    assert y.parent is None
    assert x.child is None
    assert y.child is None
    assert x.degree == 0
    assert y.degree == 0

    # execute the heap link
    heap._heap_link(y, x)

    # now node y should be a child of x
    assert y.parent is x
    assert x.child is not None

    # check if y is in the child list of x
    children = [node for node in heap._iterate_list(x.child)]
    assert y in children

    # check if the degrees have been increcesd by 1
    assert x.degree == 1

    # y is marked as False
    assert y.mark is False

    # check if x is in the root list and y is not in the root list
    root_keys = [node.key for node in heap._iterate_list(x)]
    assert y.key not in root_keys or len(root_keys) == 1  # Only x is in root list