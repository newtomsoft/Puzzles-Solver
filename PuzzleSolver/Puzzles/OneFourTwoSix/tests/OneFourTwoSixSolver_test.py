import unittest
from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.OneFourTwoSix.OneFourTwoSixSolver import OneFourTwoSixSolver

_ = OneFourTwoSixSolver.cell_empty


class OneFourTwoSixSolverTests(TestCase):
    def test_5x6_unique_solution(self):
        grid = Grid([
            [3, _, 3, _, _, _],
            [_, _, _, 1, _, _],
            [_, 1, _, _, _, _],
            [2, _, _, 2, _, 2],
            [_, _, _, 2, _, _],
            [_, 3, _, _, _, 3]
        ])
        expected_solution_str = (
            '┌───┬───────┐\n'
            '├─┐ ├─────┬─┤\n'
            '│ │ └─┐ ┌─┤ │\n'
            '│ │ ┌─┴─┘ │ │\n'
            '│ ├─┴─────┤ │\n'
            '│ └─┬─────┴─┤\n'
            '└───┴───────┘\n'
        )

        solver = OneFourTwoSixSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())
        self.assertEqual(expected_solution_str, str(solution))

    @staticmethod
    def _is_wall_edge(solution: Grid, position: Position, edge: str) -> bool:
        i, j = position.r, position.c
        if edge == "r":
            return solution[i][j] != solution[i][j + 1]
        return solution[i][j] != solution[i + 1][j]

    def test_segment_clues_consistent_solution(self):
        grid = Grid([
            [3, _, 3, _, _, _],
            [_, _, _, 1, _, _],
            [_, 1, _, _, _, _],
            [2, _, _, 2, _, 2],
            [_, _, _, 2, _, _],
            [_, 3, _, _, _, 3]
        ])
        expected_solution_str = (
            '┌───┬───────┐\n'
            '├─┐ ├─────┬─┤\n'
            '│ │ └─┐ ┌─┤ │\n'
            '│ │ ┌─┴─┘ │ │\n'
            '│ ├─┴─────┤ │\n'
            '│ └─┬─────┴─┤\n'
            '└───┴───────┘\n'
        )

        solver = OneFourTwoSixSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())

        segment_clues = [
            (Position(0, 1), "r"),
            (Position(0, 2), "b"),
            (Position(2, 2), "r"),
            (Position(2, 2), "b"),
        ]
        for position, edge in segment_clues:
            self.assertTrue(self._is_wall_edge(solution, position, edge))

        solver2 = OneFourTwoSixSolver(grid, segment_clues=segment_clues)
        solution2 = solver2.get_solution()
        self.assertEqual(expected_solution_str, str(solution2))

    def test_segment_clues_contradictory(self):
        grid = Grid([
            [3, _, 3, _, _, _],
            [_, _, _, 1, _, _],
            [_, 1, _, _, _, _],
            [2, _, _, 2, _, 2],
            [_, _, _, 2, _, _],
            [_, 3, _, _, _, 3]
        ])

        solver = OneFourTwoSixSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())

        non_wall = None
        for i in range(solution.rows_number):
            for j in range(solution.columns_number):
                for edge in ("r", "b"):
                    pos = Position(i, j)
                    try:
                        if not self._is_wall_edge(solution, pos, edge):
                            non_wall = (pos, edge)
                            break
                    except (IndexError, KeyError):
                        continue
                if non_wall:
                    break
            if non_wall:
                break
        self.assertIsNotNone(non_wall)

        solver2 = OneFourTwoSixSolver(grid, segment_clues=[non_wall])
        solution2 = solver2.get_solution()
        self.assertTrue(solution2.is_empty())


if __name__ == '__main__':
    unittest.main()