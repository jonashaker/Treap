import random

class _Node:
    def __init__(self, string, parent = None):
        """Creates new node. The priority is randomly selected from a uniform probability distribution on the intervall (0,1). Time-complexity: 0(1)"""
        self._string = string
        self._parent = parent
        self._right = None
        self._left = None
        self._priority = random.random()

    def _rotateRight(self):
        """Rotates nodes to the right according to the min-max heap rule with the requirement that the alphabetical order of nodes
        has to be preserved. Namely, the parent node has to have a higher priority than its "children". Returns the new node in the same position. Time-complexity: 0(1)"""
        root = self
        leaf = self._left
        leaf._parent = root._parent
        if leaf._parent != None:
            if leaf._parent._left == root:
                leaf._parent._left = leaf
            else:
                leaf._parent._right = leaf
        root._left = leaf._right
        if root._left != None:
            root._left._parent = root
        root._parent = leaf
        leaf._right = root
        return leaf



    def _rotateLeft(self):
        """Same as _rotateRight. But rotates the other way around. Time-complexity: 0(1)"""
        root = self
        leaf = self._right
        leaf._parent = root._parent
        if leaf._parent != None:
            if leaf._parent._right == root:
                leaf._parent._right = leaf
            else:
                leaf._parent._left = leaf
        root._right = leaf._left
        if root._right != None:
            root._right._parent = root
        root._parent = leaf
        leaf._left = root
        return leaf


class BinaryTree:
    def __init__(self):
        """Creates new binary tree. Time-complexity: 0(1)"""
        self._root = None
        self._size = 0

    def _rotate(self, root, leaf):
        """Rotates the nodes of a tree after an addition of a string to the tree has been made to achieve min-max heap property of priorities. Time-complexity: 0(n)"""
        while True:
            if root is self._root and leaf._priority > root._priority:
                if leaf._parent._left == leaf:
                    self._root = root._rotateRight()
                    self._root._parent = None
                    break
                else:
                    self._root = root._rotateLeft()
                    self._root._parent = None
                    break
            elif leaf._priority > root._priority:
                if leaf._parent._left == leaf:
                    leaf = root._rotateRight()
                else:
                    leaf = root._rotateLeft()
                root = leaf._parent
            else:
                break


    def addString(self, element):
        """Inserts a new node with given string to the tree on the right position. Time-complexity: 0(n)"""
        if self._root == None:
            self._root = _Node(element)
        else:
            root = self._root
            while True:
                """Utilizes binary search to find where new node shall be placed."""
                if element < root._string:
                    nextroot = root._left
                elif element >= root._string:
                    nextroot = root._right
                if nextroot == None:
                    leaf = _Node(element, root)
                    if element < root._string:
                        root._left = leaf
                        break
                    else:
                        root._right = leaf
                        break
                root = nextroot
            """Rotates the tree until the min-max heap property of priorities have been accomplished."""
            self._rotate(root, leaf)
        self._size += 1



    def len(self):
        """Returns size attribute of the binary tree. Same as number of nodes. Time-complexity: 0(1)"""
        return self._size

    def _orderedString(self, root):
        """Auxiliary method to orderedString. Utilizes standard method of traversal by a recursive algorithm in the binary search tree. Time-complexity: 0(log n)"""
        string = ""
        if root:
            string = self._orderedString(root._left)
            string = string + root._string + ", "
            string = string + self._orderedString(root._right)
        return string


    def orderedString(self):
        """Returns all the strings added to the binary tree in alphabetical order. Time-complexity: 0(1)"""
        if self._size >0:
            return self._orderedString(self._root)[:-2]
        else:
            return None

    def _lengthCheck(self, root):
        """Auxiliary method to healthy() which returns number of nodes in tree. Time-complexity: 0(log n)"""
        size = 0
        if root:
            size = self._lengthCheck(root._left)
            size += 1
            size += self._lengthCheck(root._right)
        return size

    def _priorityCheck(self, root):
        """Auxiliary method to healthy() to make sure the binary tree satisfy the min-max heap rule. Time-complexity: 0(log n)"""
        if root._left:
            assert root._left._priority < root._priority
            self._priorityCheck(root._left)
        if root._right:
            assert root._right._priority < root._priority
            self._priorityCheck(root._right)

    def _stringCheck(self, root):
        """Auxiliary method to healthy() to make sure that all triples and pairs of nodes satisfy the alphabetical order rule. Time-complexity: 0(log n)"""
        if root._left:
            assert root._left._string <= root._string
            self._priorityCheck(root._left)
        if root._right:
            assert root._right._string >= root._string
            self._priorityCheck(root._right)

    def healthy(self):
        """Method to make sure the binary tree is not "broken". Namely, that the number of nodes is the same as the size
        of the tree, the tree satisfies the min-max heap property of priorities and every node is positioned in alphabetical order
        with respect to its parent. Time-complexity: 0(1)"""
        assert self._size == self._lengthCheck(self._root)
        if self._size > 0:
            self._priorityCheck(self._root)
            self._root._parent == None
        else:
            assert self._root == None
        if self._size > 0:
            self._stringCheck(self._root)
        else:
            assert self._size == 0





def main():
    """Main function with testcode. Because of the randomized priorities we have to "manually" confirm that some of the methods
    works without using the addString method."""


    s = BinaryTree()
    s.healthy()
    s.addString("c")
    assert s._root._string == "c"
    s.healthy()
    s.addString("e")
    s.addString("d")
    s.addString("a")
    s.addString("k")
    s.addString("t")
    s.addString("f")
    s.addString("r")
    assert s.len() == 8
    s.healthy()

    print(s.orderedString())

    """Manually tests methods of both classes."""
    t = _Node("u")
    t._left = _Node("v", t)
    t._left._left = _Node("A", t._left)
    t._left._right = _Node("B", t._left)
    t._right = _Node("C", t)
    assert t._left._parent == t
    assert t._left._right._parent == t._left

    """Test rotateRight() method."""
    t = t._rotateRight()
    assert t._string == "v"
    assert t._left._string == "A"
    assert t._right._left._string == "B"
    assert t._right._left._parent == t._right
    assert t._right._right._string == "C"

    """Test rotateleft() method."""
    t = t._rotateLeft()
    assert t._string == "u"
    assert t._left._string == "v"
    assert t._left._left._string == "A"
    assert t._right._parent == t
    assert t._left._right._parent == t._left

    """Test _rotate() method with predetermined priorities."""
    q = BinaryTree()
    q._root = _Node("d")
    q._root._priority = 8
    q._root._right = _Node("f", q._root)
    q._root._priority_right = 7
    q._root._right._right = _Node("g", q._root._right)
    q._root._right._right._priority = 4
    q._root._right._left = _Node("e", q._root._right)
    q._root._right._left._priority = 9
    q._rotate(q._root._right, q._root._right._left)
    assert q._root._string == "e"
    assert q._root._left._string == "d"
    assert q._root._right._string == "f"
    assert q._root._right._parent == q._root

    q = BinaryTree()
    q.healthy()
    q.addString("hej")
    q.healthy()
    q.addString("pa")
    q.addString("dig")
    q.addString("min")
    q.addString("van")
    q.addString("over")
    q.addString("kom")
    q.healthy()
    print(q.len())
    print(q.orderedString())

if __name__ == '__main__':
    main()