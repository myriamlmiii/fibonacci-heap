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

    # ===== Barend's part: extract_min + consolidate =====
    def extract_min(self):
        """Remove and return the minimum key,  Amortized O(log n)."""
        z = self.min
        if z is None:
            raise IndexError("empty heap")

        # 1) Add z's children to root list
        if z.child is not None:
            children = list(self._iterate_list(z.child))
            for x in children:
                # detach from child list and move to root list
                self._remove_from_list(x)
                self._root_add(x)
                x.parent = None
                x.mark = False
            z.child = None
            z.degree = 0

        # 2) Remove z from the root list
        if z.right is z:  # z was the only root
            self.min = None
        else:
            nxt = z.right
            self._remove_from_list(z)
            self.min = nxt
            # 3) Consolidate the root list
            self._consolidate()

        self.n -= 1
        return z.key

    def _consolidate(self):
        """Link roots of the same degree until all root degrees are unique."""
        # Collect current roots (snapshot)
        roots = list(self._iterate_list(self.min))

        # Upper bound for degree array: ~ floor(log_phi(n)) + 2
        # Use a dynamic list and expand as needed.
        A = []

        def ensure_size(idx):
            if idx >= len(A):
                A.extend([None] * (idx + 1 - len(A)))

        for w in roots:
            x = w
            d = x.degree
            ensure_size(d)
            while A[d] is not None:
                y = A[d]
                if y is x:
                    break
                # Make sure x has the smaller key
                if y.key < x.key:
                    x, y = y, x
                # Link y under x
                self._heap_link(y, x)
                A[d] = None
                d = x.degree
                ensure_size(d)
            A[d] = x

        # Rebuild root list and find new min
        self.min = None
        # Clear all root list pointers and rebuild by adding each A[i]
        for a in A:
            if a is not None:
                # isolate a before adding
                a.left = a.right = a
                a.parent = None
                a.mark = False
                if self.min is None:
                    self.min = a
                else:
                    self._root_add(a)
                    if a.key < self.min.key:
                        self.min = a

    def _heap_link(self, y, x):
        """make node y a child of node x"""
        # remove y from root list
        self._remove_from_list(y)

        # add y to child list of x
        if x.child is None:
            y.left = y.right = y
            x.child = y
        
        else:
            self._insert_right(x.child, y)

        # update parent degree and mark
        y.parent = x
        y.mark = False
        x.degree += 1

    # ===== End of Barend's part =====

    # ===== Harishman's part: decrease_key, cut, cascading_cut, delete =====
    def decrease_key(self, x, new_key):
        """Decrease node x's key to new_key. Amortized O(1)."""
        if new_key > x.key:
            raise ValueError("new_key must be <= current key")
        x.key = new_key
        y = x.parent
        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if self.min is None or x.key < self.min.key:
            self.min = x

    def delete(self, x):
        """Delete node x. Amortized O(log n)."""
        self.decrease_key(x, float("-inf"))
        self.extract_min()

    def _cut(self, x, y):
        """Remove x from y's child list and add x to root list."""
        # detach x from child list
        self._remove_from_list(x)
        if y.child is x:
            y.child = x.right if x.right is not x else None
        y.degree -= 1
        # add x to root list
        self._root_add(x)
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y):
        """Perform cascading cuts up the tree."""
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)
    # ===== End of Harishman's part =====

    # ========== Internal helpers (lists / iteration) ==========
    def _root_add(self, x):
        """Add node x to the root list (next to self.min if exists)."""
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

    @staticmethod
    def _iterate_list(start):
        """Yield nodes of a circular doubly linked list starting at 'start'."""
        yield start
        cur = start.right
        while cur is not start:
            yield cur
            cur = cur.right
