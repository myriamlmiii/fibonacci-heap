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

    # ===== Baren's part: extract_min + consolidate =====
    def extract_min(self):
        # If the heap is empty, raise an error
        if self.min is None:
            raise IndexError("empty heap")
        
        # Store the minimum key to return later
        min_node = self.min

        # check if min_node has children
        if min_node.child is not None:
            # Add each child of min_node to the root list
            start = min_node.child
            while True:
                next_node = start.right
                self._root_add(start)

                # if we looped through all children break out of the loop
                if next_node == min_node.child:
                    break
                start = next_node

        # return the removed min_node
        return min_node.key
    
    def delete(self, node):
        raise NotImplementedError

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
