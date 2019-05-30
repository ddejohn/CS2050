from __future__ import print_function
import unittest


class LinkedList(object):
    class Node(object):
        # pylint: disable=too-few-public-methods
       
        def __init__(self, value, next_node):
            self.value = value
            self.next_node = next_node


    def __init__(self, args = None):
        self.front = self.back = self.current = None
        self.num_elements = 0
        if args:
            for i in args:
                self.push_front(i)

    
    def __iter__(self):
        self.current = self.front
        return self


    def __next__(self):
        if self.current:
            tmp = self.current.value
            self.current = self.current.next_node
            return tmp
        else:
            raise StopIteration()


    # Modified from an answer found on StackOverflow:
    # https://stackoverflow.com/questions/44342081
    def __repr__(self):
        if self.empty():
            return("{}({})".format(self.__class__.__name__, self.__str__()))
        else:
            return("{}(({}))".format(self.__class__.__name__, self.__str__()))


    # Modified from an answer found on StackOverflow:
    # https://stackoverflow.com/questions/19112735
    def __str__(self):
        if self.empty():
            return ""
        else:
            return " ,".join(map(str, self))[::-1]


#——————————————————————————————————————————————————————————————————————————————#


    def empty(self):
        return self.front == self.back == None

    
    def contains(self, value):
        if self.empty():
            return False
        else:
            self.current = self.front
            foo = False
            while not foo:
                if self.current.value is value:
                    foo = True
                elif self.current.next_node is not None:
                    self.current = self.current.next_node
                else:
                    break
            return foo


    def remove(self, value):
        if self.empty():
            raise RuntimeError
        
        else:
            self.num_elements -= 1

        if self.front.next_node is None:
            self.front = self.back = None
       
        elif self.front.value == value:
            self.front = self.front.next_node

        elif self.back.value == value:
            self.current = self.front
            while self.current.next_node is not self.back:
                self.current = self.current.next_node

            self.current.next_node = None
            self.back = self.current

        else:
            foo = False
            self.previous = self.front
            self.current = self.front
            self.next = self.current.next_node

            while self.current is not self.back:
                if self.current.value == value:
                    foo = True
                    break
                else:
                    self.previous = self.current
                    self.current = self.next
                    self.next = self.current.next_node

            self.previous.next_node = self.next
            self.current = None

            if not foo:
                raise ValueError("This linked list does not contain that value")
        

    def push_front(self, value):
        new = self.Node(value, self.front)
        self.num_elements += 1
        if self.empty():
            self.front = self.back = new
        else:
            self.front = new


    def pop_front(self):
        if self.empty():
            raise RuntimeError
        else:
            out = self.front.value
            self.num_elements -= 1

            if self.front is self.back:
                self.front = self.back = None
            else:
                self.front = self.front.next_node
        return out


    def push_back(self, value):
        new = self.Node(value, None)
        self.num_elements += 1
        if self.empty():
            self.front = self.back = new
        else:
            self.current = self.back
            self.current.next_node = new
            self.back = new


    def pop_back(self):
        if self.empty():
            raise RuntimeError
        
        else:
            out = self.back.value
            self.num_elements -= 1

            if self.front is self.back:
                self.front = self.back = None
            else:
                self.previous = None
                self.current = self.front
                while self.current is not self.back:
                    self.previous = self.current
                    self.current = self.current.next_node
                self.back = self.previous
        return out


    def check_types(self):
        foo = True
        first_type = type(self.front.value)
        for i in self:
            if type(i) != first_type:
                foo = False
                break
        return foo
    

    def get_middle(self):
        if self.empty() or self.num_elements % 2 == 0:
            raise RuntimeError
        else:
            self.current = self.front
            i = 0
            middle = (int)(self.num_elements/2)

            while i != middle:
                self.current = self.current.next_node
                i += 1

            return self.current.value


# ''' C-level work '''


class TestEmpty(unittest.TestCase):
    def test(self):
        self.assertTrue(LinkedList().empty())


class TestPushFrontPopBack(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_back(), 1)
        self.assertEqual(linked_list.pop_back(), 2)
        self.assertEqual(linked_list.pop_back(), 3)
        self.assertTrue(linked_list.empty())


class TestPushFrontPopFront(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        self.assertEqual(linked_list.pop_front(), 3)
        self.assertEqual(linked_list.pop_front(), 2)
        self.assertEqual(linked_list.pop_front(), 1)
        self.assertTrue(linked_list.empty())


class TestPushBackPopFront(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back(2)
        linked_list.push_back(3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_front(), 1)
        self.assertEqual(linked_list.pop_front(), 2)
        self.assertEqual(linked_list.pop_front(), 3)
        self.assertTrue(linked_list.empty())


class TestPushBackPopBack(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back("foo")
        linked_list.push_back([3, 2, 1])
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_back(), [3, 2, 1])
        self.assertEqual(linked_list.pop_back(), "foo")
        self.assertEqual(linked_list.pop_back(), 1)
        self.assertTrue(linked_list.empty())


# ''' B-level work '''


class TestInitialization(unittest.TestCase):
    def test(self):
        linked_list = LinkedList(("one", 2, 3.141592))
        self.assertEqual(linked_list.pop_back(), "one")
        self.assertEqual(linked_list.pop_back(), 2)
        self.assertEqual(linked_list.pop_back(), 3.141592)


class TestStr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__str__(), '1, 2, 3')
        linked_list = LinkedList()
        self.assertEqual(linked_list.__str__(), "")


# # ''' A-level work '''


class TestRepr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__repr__(), 'LinkedList((1, 2, 3))')
        linked_list = LinkedList()
        self.assertEqual(linked_list.__repr__(), 'LinkedList()')


class TestErrors(unittest.TestCase):
    def test_pop_front_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop_front())

    def test_pop_back_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop_back())


class TestTypes(unittest.TestCase):
    def test(self):
        linked_list = LinkedList((1, 3.14592, "cheese"))
        self.assertFalse(linked_list.check_types())

        linked_list = LinkedList((1, 2, 3))
        self.assertTrue(linked_list.check_types())


''' write some more test cases. '''

''' extra credit.
    - write test cases for and implement a delete(value) method.
    - write test cases for and implement a method that finds the middle
      element with only a single traversal.
'''

''' the following is a demonstration that uses our data structure as a
    stack'''


class TestRemove(unittest.TestCase):
    def test1(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        # self.assertEqual(str(LinkedList((1, 2, 3))), str(linked_list))
        self.assertEqual(LinkedList((1, 2, 3)).__str__(), linked_list.__str__())

    def test_remove_front(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        linked_list.remove(1)
        self.assertEqual(linked_list.__str__(), '2, 3')

    def test_remove_middle(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        linked_list.remove(2)
        self.assertEqual(linked_list.__str__(), '1, 3')

    def test_remove_back(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        linked_list.remove(3)
        self.assertEqual(linked_list.__str__(), '1, 2')
      
    def test_no_such_element(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().remove(1))
        self.assertRaises(ValueError, lambda: LinkedList((1, 2, 3)).remove(4))

    def test_emptied_list(self):
        linked_list = LinkedList((3, 2, 1))

        linked_list.remove(3)
        self.assertTrue(linked_list.__str__(), '2, 1')

        linked_list.remove(1)
        self.assertTrue(linked_list.__str__(), '2')

        linked_list.remove(2)
        self.assertTrue(linked_list.empty())


class TestGetMiddle(unittest.TestCase):
    def test1(self):
        self.assertEqual(LinkedList((1, 2, 3)).get_middle(), 2)
        self.assertRaises(RuntimeError, lambda: LinkedList((1, 2, 3, 4)).get_middle())
        self.assertRaises(RuntimeError, lambda: LinkedList().get_middle())


    def test2(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back("foo")
        linked_list.push_back([3, 2, 1])
        linked_list.push_back("[3, 2, 1]")
        linked_list.push_back(None)
        linked_list.push_back(('a', 'b', 'c'))
        linked_list.push_back(124.161)
        self.assertEqual(linked_list.get_middle(), "[3, 2, 1]")


    def test3(self):
        linked_list = LinkedList()
        linked_list.push_front(7)
        linked_list.push_front(6)
        linked_list.push_front(5)
        linked_list.push_front(4)
        linked_list.push_front(3)
        linked_list.push_front(2)
        linked_list.push_front(1)
        linked_list.remove(1)
        linked_list.remove(2)
        self.assertEqual(linked_list.get_middle(), 5)


class TestContains(unittest.TestCase):
    def test1(self):
        self.assertTrue(LinkedList((1, 2, 3)).contains(3))
        self.assertTrue(LinkedList((1, "a", 3)).contains(3))
        self.assertFalse(LinkedList((1, 2, 3)).contains("a"))
        self.assertFalse(LinkedList().contains("a"))



def fact(number):
    '''"Pretend" to do recursion via a stack and iteration'''

    if number < 0:
        raise ValueError("Less than zero")
    if number == 0 or number == 1:
        return 1

    stack = LinkedList()
    while number > 1:
        stack.push_front(number)
        number -= 1

    result = 1
    while not stack.empty():
        result *= stack.pop_front()

    return result


class TestFactorial(unittest.TestCase):
    def test_less_than_zero(self):
        self.assertRaises(ValueError, lambda: fact(-1))

    def test_zero(self):
        self.assertEqual(fact(0), 1)

    def test_one(self):
        self.assertEqual(fact(1), 1)

    def test_two(self):
        self.assertEqual(fact(2), 2)

    def test_10(self):
        self.assertEqual(fact(10), 10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1)


if '__main__' == __name__:
    unittest.main()