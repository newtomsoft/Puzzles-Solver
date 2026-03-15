import unittest
from Domain.Board.Grid import Grid
from Domain.Puzzles.Usotatami.UsotatamiSolver import UsotatamiSolver

class UsotatamiSolverTests(unittest.TestCase):
    def test_4x4(self):
        # https://gridpuzzle.com/usotatami/ov8dz
        # gpl.pq = ".|.|3|.|.|.|.|2|1|.|2|.|.|.|1|1"
        matrix = [
            [None, None, 3, None],
            [None, None, None, None],
            [None, None, None, 2],
            [1, None, 2, None]
        ]
        # Wait, 4x4 matrix is 16 elements.
        # gpl.pq = ".|.|3|.|.|.|.|2|1|.|2|.|.|.|1|1" -> 16 elements
        # 0: .  1: |  2: .  3: |
        # 4: 3  5: |  6: .  7: |
        # 8: .  9: |  10: . 11: |
        # 12: 2 13: |  14: 1 15: |
        # Actually it's simpler: it splits by |
        # ".|.|3|.|.|.|.|2|1|.|2|.|.|.|1|1".split('|') -> ['.', '.', '3', '.', '.', '.', '.', '2', '1', '.', '2', '.', '.', '.', '1', '1']

        pqq = ['.', '.', '3', '.', '.', '.', '.', '2', '1', '.', '2', '.', '.', '.', '1', '1']
        size = 4
        matrix = [[pqq[i*size + j] for j in range(size)] for i in range(size)]
        # Replace '.' with None and convert digits to int
        for r in range(size):
            for c in range(size):
                if matrix[r][c] == '.':
                    matrix[r][c] = None
                else:
                    matrix[r][c] = int(matrix[r][c])

        grid = Grid(matrix)
        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())

    def test_5x5(self):
        # https://gridpuzzle.com/usotatami/lgxp4
        # gpl.pq = "1|4|.|.|1|.|.|.|4|3|2|.|.|.|2|.|.|.|.|1|4|4|4|3|4"
        pqq = "1|4|.|.|1|.|.|.|4|3|2|.|.|.|2|.|.|.|.|1|4|4|4|3|4".split('|')
        size = 5
        matrix = [[pqq[i*size + j] for j in range(size)] for i in range(size)]
        for r in range(size):
            for c in range(size):
                if matrix[r][c] == '.':
                    matrix[r][c] = None
                else:
                    matrix[r][c] = int(matrix[r][c])

        grid = Grid(matrix)
        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())

    def test_6x6(self):
        # https://gridpuzzle.com/usotatami/yq1xk
        # gpl.pq = ".|.|2|1|2|.|.|.|1|.|.|.|5|.|.|.|.|.|2|.|1|4|.|4|3|.|.|.|3|4|4|2|.|2|1|."
        # Wait, I copied wrong earlier. Let's re-run curl if needed but I'll use this one.
        # Wait, the previous curl for 6x6 gave:
        # gpl.pq = ".|.|2|.|2|.|.|.|1|.|.|.|5|.|.|.|.|.|2|.|1|4|.|4|3|.|.|.|3|4|4|2|.|2|1|."
        pqq = ".|.|2|.|2|.|.|.|1|.|.|.|5|.|.|.|.|.|2|.|1|4|.|4|3|.|.|.|3|4|4|2|.|2|1|.".split('|')
        size = 6
        matrix = [[pqq[i*size + j] for j in range(size)] for i in range(size)]
        for r in range(size):
            for c in range(size):
                if matrix[r][c] == '.':
                    matrix[r][c] = None
                else:
                    matrix[r][c] = int(matrix[r][c])

        grid = Grid(matrix)
        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())

    def test_7x7(self):
        # https://gridpuzzle.com/usotatami/wrx2q
        # gpl.pq = ".|.|.|.|.|.|.|.|.|2|.|2|2|.|2|.|.|4|.|.|.|4|4|.|4|.|3|.|2|.|.|.|.|.|2|.|.|4|2|.|.|4|.|5|.|1|2|2|2"
        pqq = ".|.|.|.|.|.|.|.|.|2|.|2|2|.|2|.|.|4|.|.|.|4|4|.|4|.|3|.|2|.|.|.|.|.|2|.|.|4|2|.|.|4|.|5|.|1|2|2|2".split('|')
        size = 7
        matrix = [[pqq[i*size + j] for j in range(size)] for i in range(size)]
        for r in range(size):
            for c in range(size):
                if matrix[r][c] == '.':
                    matrix[r][c] = None
                else:
                    matrix[r][c] = int(matrix[r][c])

        grid = Grid(matrix)
        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())

    def test_8x8(self):
        # https://gridpuzzle.com/usotatami/pn7wv
        pqq = ".|.|.|.|5|4|.|.|3|.|.|4|1|.|.|.|1|.|.|2|.|2|.|.|4|4|2|2|.|.|4|.|.|.|.|.|3|.|.|.|1|4|3|.|.|.|.|4|.|.|.|.|2|3|.|3|3|4|.|.|.|1|2|4".split('|')
        size = 8
        matrix = [[pqq[i*size + j] for j in range(size)] for i in range(size)]
        for r in range(size):
            for c in range(size):
                if matrix[r][c] == '.':
                    matrix[r][c] = None
                else:
                    matrix[r][c] = int(matrix[r][c])

        grid = Grid(matrix)
        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())

    def test_9x9(self):
        # https://gridpuzzle.com/usotatami/0xww1
        # gpl.pq = ".|.|.|.|.|.|.|.|.|.|.|.|4|.|.|.|.|.|.|.|4|.|.|4|2|1|.|.|.|.|.|1|.|.|.|.|1|2|.|.|1|.|4|4|.|.|.|2|.|.|5|1|.|.|4|1|4|.|3|.|.|.|.|.|.|.|.|1|4|.|2|.|4|3|4|6|1|.|4|3|4"
        pqq = ".|.|.|.|.|.|.|.|.|.|.|.|4|.|.|.|.|.|.|.|4|.|.|4|2|1|.|.|.|.|.|1|.|.|.|.|1|2|.|.|1|.|4|4|.|.|.|2|.|.|5|1|.|.|4|1|4|.|3|.|.|.|.|.|.|.|.|1|4|.|2|.|4|3|4|6|1|.|4|3|4".split('|')
        size = 9
        matrix = [[pqq[i*size + j] for j in range(size)] for i in range(size)]
        for r in range(size):
            for c in range(size):
                if matrix[r][c] == '.':
                    matrix[r][c] = None
                else:
                    matrix[r][c] = int(matrix[r][c])

        grid = Grid(matrix)
        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())

if __name__ == '__main__':
    unittest.main()
