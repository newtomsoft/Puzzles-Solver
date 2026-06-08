import unittest
from unittest import TestCase
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Puzzles.RabbitsAndTrees.RabbitsAndTreesSolver import RabbitsAndTreesSolver

_ = RabbitsAndTreesSolver.cell_empty

class RabbitsAndTreesSolverTests(TestCase):
    def test_small_grid(self):
        grid = Grid([
            [_, _, 1, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        
        solver = RabbitsAndTreesSolver(grid)
        solution = solver.get_solution()
        
        self.assertFalse(solution.is_empty())
        
        for r in range(solution.rows_number):
            row = [solution.value(r, c) for c in range(solution.columns_number)]
            self.assertEqual(row.count(RabbitsAndTreesSolver.RABBIT), 1)
            self.assertEqual(row.count(RabbitsAndTreesSolver.TREE), 1)
            
        for c in range(solution.columns_number):
            col = [solution.value(r, c) for r in range(solution.rows_number)]
            self.assertEqual(col.count(RabbitsAndTreesSolver.RABBIT), 1)
            self.assertEqual(col.count(RabbitsAndTreesSolver.TREE), 1)

        self.assertNotEqual(solution.value(0, 2), RabbitsAndTreesSolver.RABBIT)

    def test_grid_hint_1(self):
        grid = Grid([
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, 1, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        
        solver = RabbitsAndTreesSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())
        
        rabbit_count = 0
        for direction in [Direction.up(), Direction.down(), Direction.left(), Direction.right()]:
            curr = Position(2, 2).after(direction)
            while 0 <= curr.r < 5 and 0 <= curr.c < 5:
                if solution.value(curr.r, curr.c) == RabbitsAndTreesSolver.TREE:
                    break
                if solution.value(curr.r, curr.c) == RabbitsAndTreesSolver.RABBIT:
                    rabbit_count += 1
                    break
                curr = curr.after(direction)
        self.assertEqual(rabbit_count, 1)

    def test_other_solution_empty_3x3(self):
        grid = Grid([[None]*3 for _ in range(3)])
        solver = RabbitsAndTreesSolver(grid)
        sol1 = solver.get_solution()
        self.assertFalse(sol1.is_empty(), "First solution should not be empty")
        
        sol2 = solver.get_other_solution()
        self.assertFalse(sol2.is_empty(), "Second solution should not be empty for an empty 3x3 grid")
        self.assertNotEqual(sol1, sol2, "Second solution must be different from the first one")

    def test_image_grid_unique_6x6(self):
        grid = Grid([
            [_, _, _, _, 1, _],
            [_, _, 1, _, _, 1],
            [2, _, _, _, 2, _],
            [_, 2, _, _, _, 1],
            [1, _, _, 1, _, _],
            [_, 2, _, _, _, _],
        ])
        solver = RabbitsAndTreesSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty(), "Solution should exist")
        
        expected = Grid([
            [0, 2, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 0],
            [0, 0, 0, 1, 0, 2],
            [2, 0, 0, 0, 1, 0],
            [0, 1, 2, 0, 0, 0],
            [0, 0, 1, 2, 0, 0],
        ])
        self.assertEqual(solution, expected)

        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty(), "There should be no other solution for this grid")

    def test_7x7_evil_vnwgd(self):
        grid = Grid([
            [_, _, _, 1, _, _, _],
            [1, _, _, _, _, _, 1],
            [_, 1, _, _, _, 1, _],
            [_, _, _, 1, _, _, _],
            [_, 2, _, _, _, 1, _],
            [2, _, _, _, _, _, 1],
            [_, _, _, 1, _, _, _],
        ])
        solver = RabbitsAndTreesSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty(), "Solution should exist for 7x7 evil")
        
        for r in range(solution.rows_number):
            row = [solution.value(r, c) for c in range(solution.columns_number)]
            self.assertEqual(row.count(RabbitsAndTreesSolver.RABBIT), 1)
            self.assertEqual(row.count(RabbitsAndTreesSolver.TREE), 1)
        for c in range(solution.columns_number):
            col = [solution.value(r, c) for r in range(solution.rows_number)]
            self.assertEqual(col.count(RabbitsAndTreesSolver.RABBIT), 1)
            self.assertEqual(col.count(RabbitsAndTreesSolver.TREE), 1)

    def test_12x12_krxdq(self):
        # Grid from https://gridpuzzle.com/rabbits-and-trees/krxdq
        grid = Grid([
            [_, _, 0, 0, _, _, _, 1, 1, _, 2, 2],
            [1, 0, _, 0, 1, 1, _, _, _, _, 2, 2],
            [_, _, 0, 0, 1, _, 0, _, 0, 1, 1, _],
            [_, 2, _, _, _, _, _, 1, 0, 1, _, 1],
            [2, _, _, _, _, 1, _, _, 0, _, _, _],
            [1, _, _, 1, 1, 1, 1, _, _, _, _, _],
            [_, _, _, _, _, 2, 2, 2, 2, _, _, 2],
            [_, _, _, 2, _, _, 1, _, _, _, _, 1],
            [2, _, 2, 2, 2, _, _, _, _, _, 2, _],
            [_, 2, 2, 2, _, 1, _, 2, 2, 2, _, _],
            [1, 2, _, _, _, _, 2, 2, 2, _, 1, 0],
            [1, 2, _, 2, 2, _, _, _, 2, 1, _, _],
        ])
        solver = RabbitsAndTreesSolver(grid)
        solution = solver.get_solution()

        expected = Grid([
            [0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0],
            [0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0],
        ])
        self.assertEqual(solution, expected)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty(), "There should be no other solution for this grid")

    def test_12x12_kr1v2(self):
        # Grid from https://gridpuzzle.com/rabbits-and-trees/kr1v2

        grid = Grid([
            [_, _, 1, _, _, _, 2, _, _, _, _, _],
            [_, _, _, 2, _, _, 2, 2, _, _, 1, _],
            [_, _, 2, _, _, _, 2, 2, _, _, _, 0],
            [2, 2, _, 2, _, _, 2, _, _, _, 1, 0],
            [_, _, _, _, _, _, 2, _, _, 2, _, _],
            [_, _, _, _, _, 2, _, 1, _, _, _, _],
            [_, _, _, _, 2, _, 2, _, _, _, _, _],
            [_, _, 2, _, 1, _, _, _, _, _, _, _],
            [2, 2, _, _, _, 2, _, _, 1, _, 1, 0],
            [2, _, _, _, 2, 2, _, _, _, 2, _, _],
            [_, 2, _, _, 2, 2, _, _, 2, _, _, _],
            [_, _, _, _, _, 2, _, _, _, 2, _, _],
        ])
        solver = RabbitsAndTreesSolver(grid)
        solution = solver.get_solution()

        expected = Grid([
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0],
            [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        ])
        self.assertEqual(solution, expected)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty(), "There should be no other solution for this grid")

if __name__ == '__main__':
    unittest.main()
