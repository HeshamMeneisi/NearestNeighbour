class KDTree(object):
    def __init__(self, data=None, partitioner=None, k=2, d_order=[0, 1]):
        """
        :param partitioner: The property to use as a partitioner. Set to None to use the direct value
        :param data: The k-dimensional vector is expected to be in the obj.[partitioner?] field
        :param force_enc: Encapsulates the supplied data points in a container with a value field
        """
        self.partitioner = partitioner
        self.k = k
        self.d_order = d_order
        self.root = None
        self.count = 0
        if data is not None and len(data) > 0:
            for obj in data:
                self.insert(obj)

    def clear(self):
        self.root = None
        self.count = 0

    def count(self):
        return self.count

    def insert(self, obj):
        """
        Same as insert_at(obj, root)
        :param obj: The k-dimensional vector is expected to be in the obj.value field
        """
        self.insert_at(obj, self.root)

    def insert_at(self, obj, target):
        """
        Insert at the specified node
        :param obj: The k-dimensional vector is expected to be in the obj.value field
        :param target: The target node. Set to None for root
        :return:
        """
        self.insert_node_at(Node(obj, self.partitioner), target)

    def insert_node_at(self, node, target):
        if target is None:
            target = self.root
        if target is None:
            self.root = node
            self.count = 1
            return
        dim = self.d_order[target.discriminator]
        if node.value[dim] < target.value[dim]:
            if target.left is None:
                node.discriminator = (target.discriminator + 1) % self.k
                target.left = node
                self.count += 1
            else:
                self.insert_node_at(node, target.left)
        else:
            if target.right is None:
                node.discriminator = (target.discriminator + 1) % self.k
                target.right = node
                self.count += 1
            else:
                self.insert_node_at(node, target.right)

    def has(self, obj):
        return self.subtree_has(Node(obj, self.partitioner), self.root)

    def subtree_has(self, node, root):
        if root is None or node is None:
            return False
        dim = self.d_order[root.discriminator]
        b = root.obj == node.obj
        if (type(b) is bool and b) or (hasattr(b, "all") and b.all()):
            return True
        if node.value[dim] < root.value[dim]:
            return self.subtree_has(node, root.left)
        else:
            return self.subtree_has(node, root.right)

    def get_root(self):
        return self.root


class BucketedKDTree(KDTree):
    # If bsize is <=0 the tree will handle bucket splitting using a climbing pointer (bsize=log(n))
    def __init__(self, data=None, partitioner=None, k=2, d_order=[0, 1], bsize=None):
        self.bsize = bsize
        super(BucketedKDTree, self).__init__(None, partitioner, k, d_order)
        base = Bucket(data, None, None)
        if bsize:
            msize = bsize
        else:
            import  math
            msize = math.log(self.count)
        self.build_tree(base, msize)

    def build_tree(self, base, bsize):
        if base.count() <= bsize:
            return base
        p = base.split()
        p.left.discriminator = p.right.discriminator = (p.discriminator+1)%self.k
        p.left = self.build_tree(p.left, bsize)
        p.right = self.build_tree(p.right, bsize)
        return p

    def insert_node_at(self, node, target):
        if target is None:
            target = self.root
        if target is None:
            self.root = Bucket([node],None, None)
            self.count = 1
            return
        if type(target) is Bucket:
            target.insert(node)
            if self.bsize is None:
                if target.p is None:
                    if target.count() >= 3:
                        n = target.split()
                        n.right.discriminator = n.left.discriminator = (n.discriminator+1)%self.k
                else:
                    target.p = target.p.parent
            elif target.count() > self.bsize:
                n = target.split()
                n.right.discriminator = n.left.discriminator = (n.discriminator + 1) % self.k
            return
        dim = self.d_order[target.discriminator]
        if node.value[dim] < target.value[dim]:
            self.insert_node_at(node, target.left)
        else:
            self.insert_node_at(node, target.right)

    def subtree_has(self, node, root):
        if root is None or node is None:
            return False
        dim = self.d_order[root.discriminator]
        if type(root) is Bucket:
            for n in root:
                b = n.obj == node.obj
                if (type(b) is bool and b) or (hasattr(b, "all") and b.all()):
                    return True
        else:
            if node.value[dim] < root.value[dim]:
                return self.subtree_has(node, root.left)
            else:
                return self.subtree_has(node, root.right)


class Node(object):
    def __init__(self, obj, partitioner=None, discriminator=0, left=None, right=None, parent=None):
        assert partitioner is None or hasattr(obj, partitioner)
        self.obj = obj
        self.partitioner = partitioner
        self.discriminator = discriminator
        self.left = left
        self.right = right
        self.parent = parent

    def __get_value(self):
        if self.partitioner is None:
            return self.obj
        return getattr(self.obj, self.partitioner)

    value = property(__get_value)


class Bucket(object):
    def __init__(self, data, p, parent, discriminator=0):
        assert data is not None, "An empty bucket is meaningless"
        self.data = data
        self.discriminator = discriminator
        self.p = p
        self.parent = parent

    def count(self):
        return len(self.data)

    def insert(self, node):
        self.data.append(node)

    def split(self):
        self.data.sort(key=lambda x: x.value[self.discriminator])
        m = len(self.data) / 2
        self.data[m].discriminator = self.discriminator
        parent = self.data[m]
        parent.parent = self.parent
        if self.parent is not None:
            if self.parent.left == self:
                self.parent.left = parent
            else:
                self.parent.right = parent
        left = Bucket(self.data[0:m], parent, parent)
        right = Bucket(self.data[m+1:], parent, parent)
        parent.left = left
        parent.right = right
        return parent
