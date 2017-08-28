class KDTree(object):
    def __init__(self, data=None, k=2, d_order=[0,1], auto_enc=False):
        """
        :param data The k-dimensional vector is expected to be in the obj.value field of each object in data
        :param auto_enc Encapsulates the supplied data points in a container with a value field
        """
        self.k = k
        self.d_order = d_order
        self.root = None
        self.count = 0
        if data is not None:
            if auto_enc:
                for point in data:
                    self.insert(Node(Container(point)))
            else:
                for obj in data:
                    self.insert(Node(obj))

    def clear(self):
        self.root = None
        self.count = 0

    def count(self):
        return self.count
    
    def insert(self, obj):
        """Same is insert_at(obj, root). Initializes the root if necessary.
        :param obj The k-dimensional vector is expected to be in the obj.value field
        """
        if self.root is None:
            self.root = obj
        self.insert_at(obj, self.root, 0)
        self.count += 1

    def insert_at(self, obj, node, d_counter):
        dim = d_counter%self.k
        if obj.value[dim] < node.obj.value[dim]:
            if node.left is None:
                node.left = Node(obj)
            else:
                self.insert_at(obj, node.left)
        else:
            if node.right is None:
                node.right = Node(obj)
            else:
                self.insert_at(obj, node.right)


class Node(object):
    def __init__(self, obj, left=None, right=None):
        self.obj = obj
        self.left = left
        self.right = right


class Container(object):
    def __init__(self, value):
        self.value = value