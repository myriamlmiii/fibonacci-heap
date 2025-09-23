import pytest
from src.fibonacci_heap import FibonacciHeap

def test_decrease_key_updates_min_and_handles_cut():
    H = FibonacciHeap()
    # Build a heap that will consolidate into a non-trivial tree:
    # Insert a bunch, then extract_min once to force consolidation.
    nodes = [H.insert(x) for x in [20, 18, 25, 7, 30, 26, 24, 23, 22, 21, 19, 17, 16, 15, 14, 13, 12]]
    H.extract_min()  # remove 7, consolidate roots

    # Pick some node that's not the min and decrease it below current min
    n = nodes[0]  # 20
    H.decrease_key(n, 5)
    assert H.minimum() == 5

def test_decrease_key_raises_if_new_key_greater():
    H = FibonacciHeap()
    n = H.insert(10)
    with pytest.raises(ValueError):
        H.decrease_key(n, 11)

def test_delete_removes_value():
    H = FibonacciHeap()
    a = H.insert(5)
    b = H.insert(9)
    c = H.insert(1)
    d = H.insert(7)
    # delete 'b' (9)
    H.delete(b)
    # extract all and ensure 9 not present
    out = []
    while H.n > 0:
        out.append(H.extract_min())
    assert 9 not in out
    assert sorted(out) == [1, 5, 7]
