import pytest
from src.fibonacci_heap import FibonacciHeap

def test_extract_min_on_empty_heap():
    """
    Test if extracting from an empty heap raises IndexError.
    """
    H = FibonacciHeap()
    with pytest.raises(IndexError):
        H.extract_min()

def test_extract_min_basic():
    H = FibonacciHeap()
    # insert random values in heap
    H.insert(5)
    H.insert(2)
    H.insert(7)
    
    # the minimum element that should be extracted is 2
    assert H.extract_min() == 2

    # after extracting the new minimum should be 5
    assert H.minimum() == 5

def test_extract_min_until_empty():
    H = FibonacciHeap()

    # insert random values in heap
    H.insert(4)
    H.insert(8)
    H.insert(3)
    H.insert(6)

    # extract min until heap is empty
    assert H.extract_min() == 3
    assert H.extract_min() == 4
    assert H.extract_min() == 6
    assert H.extract_min() == 8

    # extracting one more time should raise IndexError
    with pytest.raises(IndexError):
        H.extract_min()

