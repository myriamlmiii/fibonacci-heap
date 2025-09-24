from src.fibonacci_heap import FibonacciHeap
import pytest

def test_extract_min_on_empty_heap():
    """
    Test if extracting from an empty heap raises IndexError.
    """
    H = FibonacciHeap()
    with pytest.raises(IndexError):
        H.extract_min()

def test_extract_min_basic():
    """test extracting the minimum from a basic heap"""
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
    """test extracting till the heap is empty"""
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

def test_extract_min_sorted_sequence():
    """Full test extracting and checking if the output is sorted"""
    H = FibonacciHeap()
    data = [7, 3, 9, 1, 5, 2, 8, 6, 4]
    for x in data:
        H.insert(x)

    out = []
    while H.n > 0:
        out.append(H.extract_min())
    assert out == sorted(data)
