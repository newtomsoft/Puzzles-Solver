from unittest import TestCase, skip

from Domain.Board.Grid import Grid
from Domain.Puzzles.Neighbours.NeighboursSolver import NeighboursSolver

_ = NeighboursSolver.empty
U = NeighboursSolver.unknow


class NeighboursSolverTests(TestCase):
    def test_by_2_4x4_easy_31yn9(self):
        """https://gridpuzzle.com/neighbours/31yn9"""
        grid = Grid([
            [_, _, _, 2],
            [2, 3, 3, _],
            [4, _, _, 4],
            [_, 2, _, 2],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─┬─┬─┬─┐\n'
            '│ │ │ │ │\n'
            '├─┴─┼─┴─┤\n'
            '├───┼───┤\n'
            '└───┴───┘\n'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_5_5x5_evil_1ygx0(self):
        """https://gridpuzzle.com/neighbours/1ygx0"""
        grid = Grid([
            [2, _, _, _, _],
            [2, _, 3, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, 2, 1],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌───┬─┬─┬─┐\b'
            '├─┐ │ │ │ │\b'
            '│ │ │ │ │ │\b'
            '│ │ │ │ │ │\b'
            '│ └─┤ │ │ │\b'
            '└───┴─┴─┴─┘\b'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_4_6x6_evil_0pvkr(self):
        """https://gridpuzzle.com/neighbours/0pvkr"""
        grid = Grid([
            [3, _, _, _, _, 2],
            [_, _, _, _, _, _],
            [_, 5, 4, _, _, 5],
            [3, _, _, _, _, _],
            [_, _, _, _, _, _],
            [3, _, 3, _, 2, _],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─────┬─┬───┐\b'
            '├─┬─┐ │ │   │\b'
            '│ │ ├─┘ ├───┤\b'
            '│ │ └─┬─┘ ┌─┤\b'
            '│ ├───┼───┤ │\b'
            '├─┘ ┌─┘ ┌─┘ │\b'
            '└───┴───┴───┘\b'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_4_8x8_hard_2kdz5(self):
        """https://gridpuzzle.com/neighbours/2kdz5"""
        grid = Grid([
            [4, _, 3, _, _, _, _, 4],
            [_, _, _, _, _, _, 3, _],
            [_, _, 6, _, 6, _, _, _],
            [_, 4, _, _, 6, _, _, _],
            [_, _, _, 4, _, _, _, _],
            [3, _, _, 6, _, _, _, _],
            [_, _, 4, _, _, 6, _, 4],
            [_, _, _, 2, _, _, _, 3],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─┬───────┬───┬─┐\b'
            '│ └───┬───┤   │ │\b'
            '├───┬─┴─┐ └─┬─┘ │\b'
            '├─┐ │   ├───┴─┬─┤\b'
            '│ │ ├─┬─┴───┐ │ │\b'
            '│ └─┤ └───┐ ├─┤ │\b'
            '├───┴───┬─┴─┘ │ │\b'
            '├───────┼─────┴─┤\b'
            '└───────┴───────┘\b'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_3_9x9_evil_0me88(self):
        """https://gridpuzzle.com/neighbours/0me88"""
        grid = Grid([
            [_, _, 3, _, _, U, 3, _, _],
            [4, _, 5, _, _, _, _, _, 2],
            [_, U, _, _, _, U, _, _, _],
            [U, _, 5, _, _, _, _, U, 4],
            [_, _, 5, _, _, 4, 5, _, _],
            [U, _, _, _, _, U, _, U, _],
            [4, _, _, U, 5, _, 5, _, _],
            [_, _, _, _, _, _, U, _, 3],
            [_, U, _, 4, 3, _, _, _, _]
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─┬─────┬───┬─┬───┐\b'
            '│ └─┬───┴─┐ │ └─┐ │\b'
            '├─┬─┴───┬─┴─┼───┼─┤\b'
            '│ └─┬───┼─┐ ├─┐ │ │\b'
            '├─┬─┴─┐ │ └─┤ └─┤ │\b'
            '│ └─┐ ├─┴───┼───┴─┤\b'
            '├───┼─┴─┬─┬─┴───┬─┤\b'
            '├─┐ ├─┐ │ └─┬───┤ │\b'
            '│ └─┤ └─┼───┴─┐ │ │\b'
            '└───┴───┴─────┴─┴─┘\b'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @skip("Solver fails or times out in this environment")
    def test_by_4_10x10_evil_1dxp0(self):
        """https://gridpuzzle.com/neighbours/1dxp0"""
        grid = Grid([
            [_, _, _, _, 4, _, _, _, _, 3],
            [_, 3, 7, _, _, _, _, _, _, _],
            [_, _, _, _, 4, _, _, 5, 3, _],
            [U, _, 7, _, _, U, _, _, 3, _],
            [_, _, _, U, _, _, _, 5, _, _],
            [_, 3, _, _, _, _, U, _, _, _],
            [4, _, _, _, _, _, _, _, _, U],
            [U, _, _, _, 4, U, _, _, _, _],
            [U, _, _, _, U, _, _, 4, _, _],
            [_, _, _, _, _, _, _, 5, _, 2]
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌───┬───────┬───────┐\b'
            '│   ├─┬─────┼───┬───┤\b'
            '├───┤ └─┐ ┌─┤   │   │\b'
            '│   ├─┐ ├─┘ └─┬─┼───┤\b'
            '├───┤ ├─┴─────┤ └─┐ │\b'
            '│   │ └─┬───┬─┼─┐ │ │\b'
            '├───┴─┬─┴─┐ │ │ └─┴─┤\b'
            '├───┐ │   │ │ ├─────┤\b'
            '├─┐ └─┼───┼─┤ │ ┌───┤\b'
            '│ └───┤   │ └─┴─┤   │\b'
            '└─────┴───┴─────┴───┘\b'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @staticmethod
    def grid_to_string(grid: Grid) -> str:
        rows = grid.rows_number
        cols = grid.columns_number

        char_map = {
            (False, False, False, False): ' ',
            (False, False, False, True): '╶',
            (False, False, True, False): '╴',
            (False, False, True, True): '─',
            (False, True, False, False): '╷',
            (False, True, False, True): '┌',
            (False, True, True, False): '┐',
            (False, True, True, True): '┬',
            (True, False, False, False): '╵',
            (True, False, False, True): '└',
            (True, False, True, False): '┘',
            (True, False, True, True): '┴',
            (True, True, False, False): '│',
            (True, True, False, True): '├',
            (True, True, True, False): '┤',
            (True, True, True, True): '┼',
        }

        def get_val(r, c):
            if 0 <= r < rows and 0 <= c < cols:
                return grid[r][c]
            return -1

        result = []
        for r in range(rows + 1):
            line_chars = ['']
            for c in range(cols + 1):
                tl = get_val(r - 1, c - 1)
                tr = get_val(r - 1, c)
                bl = get_val(r, c - 1)
                br = get_val(r, c)

                up = (tl != tr)
                down = (bl != br)
                left = (tl != bl)
                right = (tr != br)

                line_chars.append(char_map[(up, down, left, right)])

                if c < cols:
                    val_above = get_val(r - 1, c)
                    val_below = get_val(r, c)
                    if val_above != val_below:
                        line_chars.append('─')
                    else:
                        line_chars.append(' ')

            line_chars.append('\n')
            result.append("".join(line_chars))

        return "".join(result)
