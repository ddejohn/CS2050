import unittest
from sys import argv

# start with solving this
SOLVE_ONE = True
# then worry about this if you have time
SOLVE_ALL = False

def safe(x1, y1, x2, y2):
    return not (x1 == x2 or y1 == y2 or abs(x2-x1) == abs(y2-y1))

def print_board(solution):
    length = len(solution)
    print(' - ' * length)

    a = [[' Q ' if (i, j) in solution else ' . ' \
        for j in range(length)] \
        for i in range(length)]
    for i in a: print(''.join(i))

    print(' - ' * length)

def solve_one(size, row, placed):
    # if we're past the last row, return placed as it has the answer.
    if row > size: return placed

    # return the empty list
    # for each column
    for col in range(size):
        # see if placing a queen at row and column is safe from all placed queens.
        for q in placed:
            # if it is safe
            if safe(row, col, q[0], q[1]):
                # make a recursive call with the next row and placed + (row, column)
                placed.append((row, col))
                solve_one(size, row + 1, placed)
                # if there was a solution with those parameters, return it.
                if len(placed) == size:
                    return placed
    return []
    
def try_again(size, placed):
    last = placed.pop()
    if last[1] == size:
        placed = try_again(size, placed)
    else:
        new = (last[0], last[1] + 1)
        s = True
        for q in placed:
            s = safe(new[0], new[1], q[0], q[1])
            if s: break
        if s:
            placed.append(new)
        else:
            placed = try_again(size, placed)
    return placed

'''
    as above, but accumulate all the solutions in the last argument.
'''
def solve_all(size, row, placed, solutions):
    pass

class test_safe(unittest.TestCase):
    def test_same(self):
        self.assertFalse(safe(1, 1, 1, 1))
    def test_same_row(self):
        self.assertFalse(safe(1, 1, 1, 2))
    def test_same_column(self):
        self.assertFalse(safe(1, 1, 2, 1))
    def test_same_diagonal(self):
        self.assertFalse(safe(1, 1, 5, 5))

class test_one(unittest.TestCase):
    def test_one_one(self):
        self.assertEqual(solve_one(1, 0, []), [(0, 0)])
    def test_two_all(self):
        self.assertEqual(solve_one(2, 0, []), [])
    def test_four_one(self):
        self.assertEqual(solve_one(4, 0, []), [(0, 1), (1, 3), (2, 0), (3, 2)])

# class test_all(unittest.TestCase):
#     def test_one_all(self):
#         self.assertEqual(solve_all(1, 0, [], []), [[(0, 0)]])
#     def test_two_all(self):
#         self.assertEqual(solve_all(2, 0, [], []), [])
#     def test_three_all(self):
#         self.assertEqual(solve_all(3, 0, [], []), [])
#     def test_four_all(self):
#         solutions = solve_all(4, 0, [], [])
#         self.assertEqual(solutions, [[(0, 1), (1, 3), (2, 0), (3, 2)], \
#             [(0, 2), (1, 0), (2, 3), (3, 1)]])


if __name__ == "__main__":
    size = 8 if len(argv) == 1 else int(argv[1])

    if SOLVE_ONE:
        print_board(solve_one(size, 0, []))
    
    if SOLVE_ALL:
        solutions = []
        solve_all(size, 0, [], solutions)
        print("there are", len(solutions), "solutions for the", \
            size, "queens problem:")
        for solution in solutions:
            print_board(solution)
