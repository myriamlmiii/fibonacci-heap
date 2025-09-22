class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False

class FibonacciHeap:
    def __init__(self):
        self.min = None

    def insert(self, key):
        raise NotImplementedError

    def minimum(self):
        raise NotImplementedError

    def merge(self, other):
        raise NotImplementedError

    def extract_min(self):
        raise NotImplementedError

    def decrease_key(self, node, new_key):
        raise NotImplementedError

    def delete(self, node):
        raise NotImplementedError
