import pytest
from src.fibonacci_heap import FibonacciHeap

def test_minimum_empty_raises():
    H = FibonacciHeap()
    with pytest.raises(IndexError):
        _ = H.minimum()

def test_insert_and_minimum_basic():
    H = FibonacciHeap()
    H.insert(5); H.insert(2); H.insert(7)
    assert H.minimum() == 2
    assert H.n == 3

def test_merge_keeps_global_min_and_size():
    A, B = FibonacciHeap(), FibonacciHeap()
    for x in [8, 3, 12]: A.insert(x)
    for y in [6, 10, 2]: B.insert(y)
    assert A.minimum() == 3 and B.minimum() == 2
    A.merge(B)
    assert A.minimum() == 2
    assert A.n == 6
