'''
Description:    Implements a Python dict, which allows for searching in
                    roughly O(1) time. There is chaining however, so 
                    search times may be slightly decreased from O(1)
Author:         Devon DeJohn
Version:        0.9.9

C-level work - done
    Implement __len__()
    Implement __setitem__()
    Implement __getitem__()
    Implement __contains__()

B-level work - done
    Add doubling and rehashing when load goes over 75%
    Add __delitem__(self, key)

A-level work - done
    Add halving and rehashing when load goes below 25%
    Add keys()
    Add values()

Extra credit - done
    Add __eq__()
    Add items(), 'a list of D's (key, value) pairs, as 2-tuples'
'''

import unittest

class dictionary:
    def __init__(self, init=None):
        self.__limit = 10
        self.__count = 0
        self.__items = [[] for __ in range(self.__limit)]

        if init:
            for i in init:
                self.__setitem__(i[0], i[1])

    # With help from Wright#9072 and Poke#0002 in the python discord
    def __len__(self):
        ''' Generator expressions are pretty. '''
        return sum(bool(i) for i in self.flattened())
            
    def __iter__(self):  
        return(iter(self.flattened())) 
    
    def __str__(self): 
        return(str(self.flattened()))

    def __setitem__(self, key, value):
        ''' Add to the dictionary. '''
        load_factor = self.__count / self.__limit
        
        if load_factor >= 0.75:
            self.__limit *= 2
            self.rehash()

        if not key in self:
            self.__items[self.slot(key)].append((key, value))    
            self.__count += 1

        else:
            print('\nThat key already existed. Its corresponding value has been overwritten.\n')
            for i in self.__items[self.slot(key)]:
                if i[0] == key:
                    self.__items[self.slot(key)] = [(key, value)]

    # With help from Lord Zondo#2199 in the python discord, on using generator functions
    def __getitem__(self, key):
        ''' Retrieve from the dictionary. '''
        return next(i[1] for i in self.__items[self.slot(key)] if i[0] == key)

    def __delitem__(self, key):
        if key in self.keys():
            slot = self.__items[self.slot(key)]

            for i in range(len(slot)):
                if slot[i][0] == key:
                    del slot[i]
                    self.__count -= 1

            load_factor = self.__count / self.__limit
            
            if load_factor <= 0.25:
                self.__limit //= 2
                self.rehash()
        else:
            raise KeyError('Key not found')
    
    def __eq__(self, d):
        return self.items() == d.items()

    def __contains__(self, key):
        ''' Implements the 'in' operator. '''
        return key in self.keys()

    def flattened(self):
        return [item for inner in self.__items for item in inner]

    def keys(self):
        return [k[0] for k in self.items()]

    def values(self):
        return [k[1] for k in self.items()]

    def items(self):
        return self.flattened()

    def slot(self, key):
        return hash(key) % self.__limit

    def rehash(self):
        old = self.flattened()
        self.__count = 0
        self.__items = [[] for __ in range(self.__limit)]

        for i in old:
            self.__setitem__(i[0], i[1])

    def prnt(self):
        print('')
        print(self.__items)

class test_add_two(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = 'one'
        s[2] = 'two'
        self.assertEqual(len(s), 2)
        self.assertEqual(s[1], 'one')
        self.assertEqual(s[2], 'two')

class test_add_twice(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = 'one'
        s[1] = 'two'
        self.assertEqual(len(s), 1)
        self.assertEqual(s[1], 'two')

class test_store_none(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = None
        self.assertTrue(1 in s)
        self.assertEqual(s[1], None)
        
class test_none_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[None] = 1
        self.assertTrue(None in s)
        self.assertEqual(s[None], 1)
        
class test_store_false(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = False
        self.assertTrue(1 in s)
        self.assertFalse(s[1])

class test_false_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[False] = 1
        self.assertTrue(False in s)
        self.assertEqual(s[False], 1)
        
class test_collide(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = 'zero'
        s[10] = 'ten'
        self.assertEqual(len(s), 2)
        self.assertTrue(0 in s)
        self.assertTrue(10 in s)

class test_double(unittest.TestCase):
    def test(self):
        s = dictionary()
        num_words = 'zero one two three four five six seven eight nine ten'.split()
        for i in range(len(num_words)):
            s[i] = num_words[i]

        self.assertEqual(len(s), 11)
        self.assertTrue(0 in s)
        self.assertTrue(10 in s)
       
class test_big_dict(unittest.TestCase):
    def test(self):
        s = dictionary()
        specials = 'zero ten -hundred'.split()
        nums = 'one two three four five six seven eight nine'.split()
        teens = 'ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
        prefixes = 'twenty- thirty- forty- fifty- sixty- seventy- eighty- ninety-'.split()

        for i in range(110):
            if i == 0:
                val = specials[0]
            elif i < 10:
                val = nums[i - 1]
            elif i < 20:
                val = teens[i % 10]
            elif i % 10 == 0 and i != 100:
                val = prefixes[int(i/10) - 2].strip('-')
            elif i < 100:
                val = prefixes[int(i/10) - 2] + nums[(i - 10*int(i/10) - 1) % 9]
            else:
                if i == 100:
                    val = nums[0] + specials[2]
                else:
                    val = nums[0] + specials[2] + ' ' + nums[(i - 101) % 9]
            s[i] = val

class test_del(unittest.TestCase):
    def test(self):
        s = dictionary()
        num_words = 'zero one two three four five six seven eight nine ten'.split()
        for i in range(len(num_words)):
            s[i] = num_words[i]

        del s[10]
        del s[1]
        del s[5]
        del s[8]
        del s[3]
        del s[2]
        del s[0]
        del s[7]
        
        self.assertEqual([(4, 'four'), (6, 'six'), (9, 'nine')], s.items())

class test_non_int_keys(unittest.TestCase):
    def test(self):
        s = dictionary()
        keys = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
        for i in range(len(keys)):
            s[keys[i]] = i

class test_del_no_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = 'zero'
        s[1] = 'one'
        s[2] = 'two'
        with self.assertRaises(KeyError):
            del s['abc']

class test_weird_keys(unittest.TestCase):
    def test(self):
        s = dictionary()
        weird_keys = [None, False, '', ' ', 6.28, 1, 'a', '1', True]
        num_words = 'zero one two three four five six seven eight'.split()
        for i in range(len(weird_keys)):
            s[weird_keys[i]] = num_words[i]
        print(s.keys())
        # self.assertEqual(7, len(s))

class test_halve(unittest.TestCase):
    def test(self):
        s = dictionary()
        num_words = 'zero one two three four five six seven eight nine ten'.split()
        for i in range(len(num_words)):
            s[i] = num_words[i]

        for i in range(9):
            del s[i]
        
        self.assertEqual(2, len(s))

class test_keys(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = 'zero'
        s[1] = 'one'
        s[2] = 'two'
        self.assertEqual([0, 1, 2], s.keys())

class test_vals(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = 'zero'
        s[1] = 'one'
        s[2] = 'two'
        self.assertEqual(['zero', 'one', 'two'], s.values())

class test_items(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = 'zero'
        s[1] = 'one'
        s[2] = 'two'
        self.assertEqual([(0, 'zero'), (1, 'one'), (2, 'two')], s.items())

class test_init(unittest.TestCase):
    def test(self):
        s = dictionary([('one', 1), ('two', 2), ('three', 3)])
        s.prnt()
        self.assertEqual(len(s), 3)

class test_eq(unittest.TestCase):
    def test(self):
        a = dictionary()
        a[0] = 'zero'
        a[1] = 'one'
        a[2] = 'two'

        b = dictionary()
        b[0] = 'zero'
        b[1] = 'one'
        b[2] = 'two'

        c = dictionary()
        c[0] = 'foo'
        c[1] = 'bar'
        c[2] = 'baz'
        self.assertTrue(a == b != c)
        self.assertFalse(a == c)

unittest.main()
