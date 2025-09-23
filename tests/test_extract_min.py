from src.fibonacci_heap import FibonacciHeap

def test_extract_min_sorted_sequence():
    H = FibonacciHeap()
    data = [7, 3, 9, 1, 5, 2, 8, 6, 4]
    for x in data:
        H.insert(x)

    out = []
    while H.n > 0:
        out.append(H.extract_min())
    assert out == sorted(data)
