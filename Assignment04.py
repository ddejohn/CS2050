import unittest

class binary_search_tree:
    def __init__ (self, init=None):
        self.__value = self.__left = self.__right = None

        if init:
            for i in init:
                self.add(i)

    def __iter__(self):
        if self.__left:
            for node in self.__left:
                yield(node)

        yield(self.__value)

        if self.__right:
            for node in self.__right:
                yield(node)

    def __str__(self): 
        return(', '.join(str(node) for node in self))

    def add(self, value):
        # if this is the first value for this node, just set to node's value
        if not self.__value:
            self.__value = value
        # if the value is less than this node's value
        elif value < self.__value:
            # if there isn't a left
            if not self.__left:
                # create a new tree and have left refer to it
                self.__left = binary_search_tree([value])
            else:
                self.__left.add(value)
        else:
            if not self.__right:
                # create a new tree and have right refer to it
                self.__right = binary_search_tree([value])
            else:
                # make a recursive call
                self.__right.add(value)

    def preorder(self):
        res = []
        res += [self.__value]
        if self.__left:
            res += self.__left.preorder()
        if self.__right:
            res += self.__right.preorder()
        return res

    def inorder(self):
        res = []
        if self.__left:
            res += self.__left.inorder()
        res += [self.__value]
        if self.__right:
            res += self.__right.inorder()
        return res

    def postorder(self):
        res = []
        if self.__left:
            res += self.__left.postorder()
        if self.__right:
            res += self.__right.postorder()
        res += [self.__value]
        return res

    def BFS(self):
        # create a queue to hold trees
        q = [self]
        # create an empty list to hold roots
        res = []
        #while there are nodes in the queue
        while q:
            # grab the first one and add it to the result list
            k = q.pop(0)
            res.append(k.__value)
            # if there is a node to the left, add that to the queue
            if k.__left:
                q.append(k.__left)
            # if there is a node to the right, add that to the queue
            if k.__right:
                q.append(k.__right)
        return res

class test_binary_search_tree (unittest.TestCase):
    '''
       20
      /  \
     10  30
        /  \
       25  35
    '''
    # C level
    def test_empty(self):
        self.assertEqual(str(binary_search_tree()), 'None')
    
    def test_one(self):
        self.assertEqual(str(binary_search_tree([1])), '1')
    
    def test_add(self):
        bt = binary_search_tree()
        bt.add(20)
        bt.add(10)
        bt.add(30)
        bt.add(25)
        bt.add(35)
        self.assertEqual(str(bt), '10, 20, 25, 30, 35')

    def test_init(self):
        bt = binary_search_tree([20, 10, 30, 25, 35])
        self.assertEqual(str(bt), '10, 20, 25, 30, 35')

    # B level
    def test_empty_inorder(self):
        self.assertEqual(binary_search_tree().inorder(), [None])
    
    def test_postorder(self):
        bt = binary_search_tree([20, 10, 30, 25, 35])
        self.assertEqual(bt.postorder(), [10, 25, 35, 30, 20])
    
    def test_inorder(self):
        bt = binary_search_tree([20, 10, 30, 25, 35])
        self.assertEqual(bt.inorder(), [10, 20, 25, 30, 35])
    
    # this preorder works
    def test_preorder(self):
        bt = binary_search_tree([20, 10, 30, 25, 35])
        self.assertEqual(list(bt.preorder()), [20, 10, 30, 25, 35])
    
    # this preorder does NOT work
    def test_big_tree(self):
        bt = binary_search_tree([20, 10, 5, 2, 6, 30, 31, 25, 26, 27, 1, 35, 14])
        self.assertEqual(bt.preorder(), [20, 10, 5, 2, 1, 6, 14, 30, 25, 26, 27, 31, 35])
        self.assertEqual(bt.inorder(), [1, 2, 5, 6, 10, 14, 20, 25, 26, 27, 30, 31, 35])
        self.assertEqual(bt.postorder(), [1, 2, 6, 5, 14, 10, 27, 26, 25, 35, 31, 30, 20])

    # A level
    def test_empty_BFS(self):
        self.assertEqual(binary_search_tree().BFS(), [None])
    
    def test_BFS(self):
        bt = binary_search_tree([20, 10, 30, 25, 35])
        self.assertEqual(bt.BFS(), [20, 10, 30, 25, 35])

    def test_big_BFS(self):
        bt = binary_search_tree([20, 10, 5, 2, 6, 30, 31, 25, 26, 27, 1, 35, 14])
        self.assertEqual(bt.BFS(), [20, 10, 30, 5, 14, 25, 31, 2, 6, 26, 35, 1, 27])

if '__main__' == __name__:
    unittest.main()