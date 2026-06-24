import unittest
from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
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

        solver = OneFourTwoSixSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())

    @staticmethod
    def _wall_value(solution: Grid, edge: str, i: int, j: int) -> int:
        if edge == "r":
            return 1 if solution[i][j] != solution[i][j + 1] else 0
        return 1 if solution[i][j] != solution[i + 1][j] else 0

    def test_segment_clues_consistent_solution(self):
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

        segment_clues = {
            "r:0:0": self._wall_value(solution, "r", 0, 0),
            "b:0:0": self._wall_value(solution, "b", 0, 0),
        }
        solver2 = OneFourTwoSixSolver(grid, segment_clues=segment_clues)
        solution2 = solver2.get_solution()
        self.assertFalse(solution2.is_empty())
        self.assertEqual(
            solution2.normalize_regions().matrix,
            solution.normalize_regions().matrix,
        )

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

        opposite = 1 - self._wall_value(solution, "r", 0, 0)
        segment_clues = {"r:0:0": opposite}
        solver2 = OneFourTwoSixSolver(grid, segment_clues=segment_clues)
        solution2 = solver2.get_solution()
        self.assertTrue(solution2.is_empty())

    def test_segment_clues_unique_with_other_solution(self):
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

        segment_clues = {
            "r:0:0": self._wall_value(solution, "r", 0, 0),
            "b:1:0": self._wall_value(solution, "b", 1, 0),
            "r:2:1": self._wall_value(solution, "r", 2, 1),
        }
        solver2 = OneFourTwoSixSolver(grid, segment_clues=segment_clues)
        solution2 = solver2.get_solution()
        self.assertFalse(solution2.is_empty())
        other = solver2.get_other_solution()
        self.assertTrue(other.is_empty())


if __name__ == '__main__':
    unittest.main()
