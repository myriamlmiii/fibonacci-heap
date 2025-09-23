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
        # If the heap is empty, raise an error
        if self.min is None:
            raise IndexError("empty heap")
        
        # Store the minimum key to return later
        min_node = self.min

        # if node has children, add them to the root list
        if min_node.child is not None:
            # Add each child of min_node to the root list
            children = [child for child in self._iterate_list(min_node.child)]
            for child in children:
                self._root_add(child)
                child.parent = None

        # Remove min_node from the root list
        self._remove_from_list(min_node)

        # update self.min and consolidate
        if min_node == min_node.right:  # only node in the root list
            self.min = None
        else:
            self.min = min_node.right
            self._consolidate()

        # decrease the node count in heap
        self.n -= 1

        # return the removed min_node
        return min_node.key
    
    def _consolidate(self):
        """Combines trees of the same degree, so no roots have the same degree."""
        # used to track nodes by degree
        A = {} 

        # put all root nodes in a list
        root_nodes = [node for node in self._iterate_list(self.min)]

        for i in root_nodes:
            x = i
            d = x.degree
            
            # while there is another node with the same degree
            while d in A:
                y = A[d] # get the node with the same degree
                if y.key < x.key: # make sure x has the smaller key
                    x, y = y, x
                # merge the two trees, y becomes a child of x
                self._heap_link(y, x)
                # remove the entery of the degrees dictionary
                del A[d]
                # increse the number of childs of x, since we just added one
                d += 1

                A[d] = x  # add x to the dictionary with its new degree

        # Rebuild the root list from roots in A, and find the new minimum
        self.min = None
        for node in A.values():
            node.left = node.right = node  # Detach from any previous list
            if self.min is None:
                self.min = node
            else:
                # Insert node into the root list
                self._insert_right(self.min, node)
                # Update self.min if this node has a smaller key
                if node.key < self.min.key:
                    self.min = node

    def _heap_link(self, y, x):
        """"make node y a child of node x."""
        # remove y from root list
        self._remove_from_list(y)

        # make y a child of x
        y.left = y.right = y
        if x.child is None:
            x.child = y
        else:
            self._insert_right(x.child, y)
        
        # update parent, degree, and mark
        y.parent = x
        x.degree += 1
        y.mark = False

    # ===== End of Barend's part =====

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
