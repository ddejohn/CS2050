import unittest

'''
Description:    Finds and replaces a desired word or char in a given string
Author:         Devon DeJohn
Version:        1.0
'''

def whole_word_replace(find, replace, string):
    if find and string and replace is not None:
        if string == '':
            return string

        build = ''
        words = string.split()

        if words[0] == find:
            build += replace + ' ' + whole_word_replace(find, replace, ' '.join(map(str, words[1:])))

        else:
            build += words[0] + ' ' + whole_word_replace(find, replace, ' '.join(map(str, words[1:])))
            
        return build.strip()    # easier to strip off the last space than write logic to avoid it altogether
    
    else: return string


def findandreplace(find, replace, string):
    if find and string and replace is not None:
        if string == '':
            return string

        build = ''
        if string[:len(find)] == find:
            build += replace + findandreplace(find, replace, string[len(find):])

        else:
            build += string[:1] + findandreplace(find, replace, string[1:])
            
        return build
    
    else: return string

class TestFindAndReplace(unittest.TestCase):
    def test_all_none(self):
        self.assertEqual(findandreplace(None, None, None), None)
        print('')
        print('given: None')
        print('want:  None')
        print('got:  ', findandreplace(None, None, None))

    def test_find_none(self):
        self.assertEqual(findandreplace(None, 'a', 'aabb'), 'aabb')
        print('')
        print('given: aabb')
        print('want:  aabb')
        print('got:  ', findandreplace(None, 'a', 'aabb'))

    def test_find_empty(self):
        self.assertEqual(findandreplace('', 'a', 'aabb'), 'aabb')
        print('')
        print('given: aabb')
        print('want:  aabb')
        print('got:  ', findandreplace('', 'a', 'aabb'))

    def test_replace_none(self):
        self.assertEqual(findandreplace('a', None, 'aabb'), 'aabb')
        print('')
        print('given: aabb')
        print('want:  aabb')
        print('got:  ', findandreplace('a', None, 'aabb'))

    def test_string_none(self):
        self.assertEqual(findandreplace('a', 'b', None), None)
        print('')
        print('given: None')
        print('want:  None')
        print('got:  ', findandreplace('a', 'b', None))

    def test_simple(self):
        self.assertEqual(findandreplace('a', 'b', 'aabb'), 'bbbb')
        print('')
        print('given: aabb')
        print('want:  bbbb')
        print('got:  ', findandreplace('a', 'b', 'aabb'))

    def test_remove(self):
        self.assertEqual(findandreplace(' ', '', ' a abb'), 'aabb')
        print('')
        print('given: \' a abb\'')
        print('want:  aabb')
        print('got:  ', findandreplace(' ', '', ' a abb'))

    def test_gettysburg(self):
        self.assertEqual(findandreplace('Four score', 'Twenty', \
            'Four score and seven years ago'), 'Twenty and seven years ago')
        print('')
        print('given: Four score and seven years ago')
        print('want:  Twenty and seven years ago')
        print('got:  ', findandreplace('Four score', 'Twenty', \
            'Four score and seven years ago'))

# lazy whole-word matching
class TestWholeWordMatch(unittest.TestCase):
    def test_replace_whole_word(self):
        find = 'ant'
        replace = 'foo'
        string = 'lycanthropic ant farm anthropology'
        want = 'lycanthropic foo farm anthropology'
        print('')
        print('given:', string)
        print('want: ', want)
        print('got:  ', whole_word_replace(find, replace, string))
        self.assertEqual(whole_word_replace(find, replace, string), want)


unittest.main()  
