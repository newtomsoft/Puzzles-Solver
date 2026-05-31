# import unittest
# from unittest import TestCase
#
# from PuzzleSolver.Board.Grid import Grid
# from PuzzleSolver.Puzzles.BattleshipsRetrograde.BattleshipsRetrogradeSolver import BattleshipsRetrogradeSolver
#
# _ = -1
#
#
# class BattleshipsRetrogradeSolverTests(TestCase):
#     def test_solution_7x7_hard_0y8g2(self):
#         """https://gridpuzzle.com/battleships-retrograde/0y8g2"""
#         grid = Grid([
#             [3, 8, 4, 3, 4, 7, 1],
#             [1, 3, 8, 8, 4, 7, 8],
#             [8, 3, 4, 3, 4, 1, 2],
#             [2, 7, 3, 4, 7, 8, 1],
#             [7, 3, 8, 4, 7, 2, 2],
#             [3, 4, 3, 8, 4, 7, 7],
#             [7, 3, 4, 7, 3, 4, 7],
#         ])
#         ships_number_by_size = {1: 3, 2: 2, 3: 1, 4: 1}
#
#         expected_solution = Grid([
#             [0, 0, 0, 0, 0, 0, 0],
#             [0, 3, 6, 6, 4, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 3, 4, 0, 0, 1],
#             [7, 0, 0, 0, 0, 0, 2],
#             [0, 0, 3, 6, 4, 0, 0],
#             [7, 0, 0, 0, 0, 0, 7],
#         ])
#
#         solver = BattleshipsRetrogradeSolver(grid, ships_number_by_size)
#         solution = solver.get_solution()
#         self.assertEqual(expected_solution, solution)
#         self.assertEqual(Grid.empty(), solver.get_other_solution())
#
#
# if __name__ == '__main__':
#     unittest.main()
