class Node:
    __slots__ = ("key", "degree", "parent", "child", "left", "right", "mark")

    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False


class FibonacciHeap:
    def __init__(self):
        self.min = None
        self.n = 0

    # ===== Meriem's part =====
    def insert(self, key):
        x = Node(key)
        self._root_add(x)
        if self.min is None or key < self.min.key:
            self.min = x
        self.n += 1
        return x

    def minimum(self):
        if self.min is None:
            raise IndexError("empty heap")
        return self.min.key

    def merge(self, other):
        if other is None or other.min is None:
            return
        if self.min is None:
            self.min = other.min
            self.n = other.n
            return
        self._concat_root_lists(self.min, other.min)
        if other.min.key < self.min.key:
            self.min = other.min
        self.n += other.n
    # ===== End of Meriem's part =====

    def extract_min(self):
        raise NotImplementedError

    def decrease_key(self, node, new_key):
        raise NotImplementedError

    def delete(self, node):
        raise NotImplementedError

    def _root_add(self, x):
        if self.min is None:
            x.left = x.right = x
        else:
            self._insert_right(self.min, x)
        x.parent = None
        x.mark = False

    @staticmethod
    def _insert_right(a, x):
        x.left = a
        x.right = a.right
        a.right.left = x
        a.right = x

    @staticmethod
    def _remove_from_list(x):
        x.left.right = x.right
        x.right.left = x.left
        x.left = x.right = x

    @staticmethod
    def _concat_root_lists(a, b):
        a_r = a.right
        b_l = b.left
        a.right = b
        b.left = a
        a_r.left = b_l
        b_l.right = a_r
