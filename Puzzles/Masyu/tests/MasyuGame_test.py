from unittest import TestCase

from Puzzles.Masyu.MasyuGame import MasyuGame
from Utils.Grid import Grid
from Utils.Island import Island
from Utils.Position import Position


class MasyuGameTests(TestCase):
    def test_solution_white_0(self):
        grid = Grid([
            [' ', 'w', ' '],
            [' ', 'w', ' '],
        ])

        game = MasyuGame(grid)
        solution = game.get_solution()

        expected_island_0_0 = Island(Position(0, 0), 2)
        expected_island_0_1 = Island(Position(0, 1), 2)
        expected_island_0_2 = Island(Position(0, 2), 2)
        expected_island_1_0 = Island(Position(1, 0), 2)
        expected_island_1_1 = Island(Position(1, 1), 2)
        expected_island_1_2 = Island(Position(1, 2), 2)

        expected_island_0_0.set_bridge(Position(0, 1), 1)
        expected_island_0_0.set_bridge(Position(1, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 2), 1)
        expected_island_0_2.set_bridge(Position(1, 2), 1)
        expected_island_0_2.set_bridge(Position(0, 1), 1)
        expected_island_1_0.set_bridge(Position(0, 0), 1)
        expected_island_1_0.set_bridge(Position(1, 1), 1)
        expected_island_1_1.set_bridge(Position(1, 0), 1)
        expected_island_1_1.set_bridge(Position(1, 2), 1)
        expected_island_1_2.set_bridge(Position(0, 2), 1)
        expected_island_1_2.set_bridge(Position(1, 1), 1)

        expected_solution = Grid([
            [expected_island_0_0, expected_island_0_1, expected_island_0_2],
            [expected_island_1_0, expected_island_1_1, expected_island_1_2]
        ])

        self.assertEqual(expected_solution, solution)

        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_1(self):
        grid = Grid([
            [' ', 'w', ' '],
            [' ', ' ', ' '],
            [' ', 'w', ' '],
        ])

        game = MasyuGame(grid)
        solution = game.get_solution()

        expected_island_0_0 = Island(Position(0, 0), 2)
        expected_island_0_1 = Island(Position(0, 1), 2)
        expected_island_0_2 = Island(Position(0, 2), 2)
        expected_island_1_0 = Island(Position(1, 0), 2)
        expected_island_1_1 = Island(Position(1, 1), 0)
        expected_island_1_2 = Island(Position(1, 2), 2)
        expected_island_2_0 = Island(Position(2, 0), 2)
        expected_island_2_1 = Island(Position(2, 1), 2)
        expected_island_2_2 = Island(Position(2, 2), 2)

        expected_island_0_0.set_bridge(Position(0, 1), 1)
        expected_island_0_0.set_bridge(Position(1, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 2), 1)
        expected_island_0_2.set_bridge(Position(1, 2), 1)
        expected_island_0_2.set_bridge(Position(0, 1), 1)
        expected_island_1_0.set_bridge(Position(0, 0), 1)
        expected_island_1_0.set_bridge(Position(2, 0), 1)
        expected_island_1_2.set_bridge(Position(0, 2), 1)
        expected_island_1_2.set_bridge(Position(2, 2), 1)
        expected_island_2_0.set_bridge(Position(2, 1), 1)
        expected_island_2_0.set_bridge(Position(1, 0), 1)
        expected_island_2_1.set_bridge(Position(2, 2), 1)
        expected_island_2_1.set_bridge(Position(2, 0), 1)
        expected_island_2_2.set_bridge(Position(2, 1), 1)
        expected_island_2_2.set_bridge(Position(1, 2), 1)

        expected_solution = Grid([
            [expected_island_0_0, expected_island_0_1, expected_island_0_2],
            [expected_island_1_0, expected_island_1_1, expected_island_1_2],
            [expected_island_2_0, expected_island_2_1, expected_island_2_2]
        ])

        self.assertEqual(expected_solution, solution)

        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_2(self):
        grid = Grid([
            [' ', 'w', ' ', ' '],
            ['w', ' ', ' ', 'w'],
            [' ', ' ', 'w', ' '],
        ])

        game = MasyuGame(grid)
        solution = game.get_solution()

        expected_island_0_0 = Island(Position(0, 0), 2)
        expected_island_0_1 = Island(Position(0, 1), 2)
        expected_island_0_2 = Island(Position(0, 2), 2)
        expected_island_0_3 = Island(Position(0, 3), 2)
        expected_island_1_0 = Island(Position(1, 0), 2)
        expected_island_1_1 = Island(Position(1, 1), 0)
        expected_island_1_2 = Island(Position(1, 2), 0)
        expected_island_1_3 = Island(Position(1, 3), 2)
        expected_island_2_0 = Island(Position(2, 0), 2)
        expected_island_2_1 = Island(Position(2, 1), 2)
        expected_island_2_2 = Island(Position(2, 2), 2)
        expected_island_2_3 = Island(Position(2, 3), 2)

        expected_island_0_0.set_bridge(Position(0, 1), 1)
        expected_island_0_0.set_bridge(Position(1, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 2), 1)
        expected_island_0_2.set_bridge(Position(0, 1), 1)
        expected_island_0_2.set_bridge(Position(0, 3), 1)
        expected_island_0_3.set_bridge(Position(0, 2), 1)
        expected_island_0_3.set_bridge(Position(1, 3), 1)
        expected_island_1_0.set_bridge(Position(0, 0), 1)
        expected_island_1_0.set_bridge(Position(2, 0), 1)
        expected_island_1_3.set_bridge(Position(0, 3), 1)
        expected_island_1_3.set_bridge(Position(2, 3), 1)
        expected_island_2_0.set_bridge(Position(1, 0), 1)
        expected_island_2_0.set_bridge(Position(2, 1), 1)
        expected_island_2_1.set_bridge(Position(2, 0), 1)
        expected_island_2_1.set_bridge(Position(2, 2), 1)
        expected_island_2_2.set_bridge(Position(2, 1), 1)
        expected_island_2_2.set_bridge(Position(2, 3), 1)
        expected_island_2_3.set_bridge(Position(1, 3), 1)
        expected_island_2_3.set_bridge(Position(2, 2), 1)

        expected_solution = Grid([
            [expected_island_0_0, expected_island_0_1, expected_island_0_2, expected_island_0_3],
            [expected_island_1_0, expected_island_1_1, expected_island_1_2, expected_island_1_3],
            [expected_island_2_0, expected_island_2_1, expected_island_2_2, expected_island_2_3]
        ])

        self.assertEqual(expected_solution, solution)

        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black(self):
        grid = Grid([
            ['b', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', 'b'],
        ])

        game = MasyuGame(grid)
        solution = game.get_solution()

        expected_island_0_0 = Island(Position(0, 0), 2)
        expected_island_0_1 = Island(Position(0, 1), 2)
        expected_island_0_2 = Island(Position(0, 2), 2)
        expected_island_1_0 = Island(Position(1, 0), 2)
        expected_island_1_1 = Island(Position(1, 1), 0)
        expected_island_1_2 = Island(Position(1, 2), 2)
        expected_island_2_0 = Island(Position(2, 0), 2)
        expected_island_2_1 = Island(Position(2, 1), 2)
        expected_island_2_2 = Island(Position(2, 2), 2)

        expected_island_0_0.set_bridge(Position(0, 1), 1)
        expected_island_0_0.set_bridge(Position(1, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 2), 1)
        expected_island_0_2.set_bridge(Position(0, 1), 1)
        expected_island_0_2.set_bridge(Position(1, 2), 1)
        expected_island_1_0.set_bridge(Position(0, 0), 1)
        expected_island_1_0.set_bridge(Position(2, 0), 1)
        expected_island_1_2.set_bridge(Position(0, 2), 1)
        expected_island_1_2.set_bridge(Position(2, 2), 1)
        expected_island_2_0.set_bridge(Position(1, 0), 1)
        expected_island_2_0.set_bridge(Position(2, 1), 1)
        expected_island_2_1.set_bridge(Position(2, 0), 1)
        expected_island_2_1.set_bridge(Position(2, 2), 1)
        expected_island_2_2.set_bridge(Position(2, 1), 1)
        expected_island_2_2.set_bridge(Position(1, 2), 1)

        expected_solution = Grid([
            [expected_island_0_0, expected_island_0_1, expected_island_0_2],
            [expected_island_1_0, expected_island_1_1, expected_island_1_2],
            [expected_island_2_0, expected_island_2_1, expected_island_2_2]
        ])

        self.assertEqual(expected_solution, solution)

        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_grid(self):
        grid = Grid([
            ['b', ' ', 'w', ' '],
            [' ', ' ', 'w', ' '],
            [' ', ' ', ' ', ' ']
        ])

        game = MasyuGame(grid)
        solution = game.get_solution()

        expected_island_0_0 = Island(Position(0, 0), 2)
        expected_island_0_1 = Island(Position(0, 1), 2)
        expected_island_0_2 = Island(Position(0, 2), 2)
        expected_island_0_3 = Island(Position(0, 3), 2)
        expected_island_1_0 = Island(Position(1, 0), 2)
        expected_island_1_1 = Island(Position(1, 1), 2)
        expected_island_1_2 = Island(Position(1, 2), 2)
        expected_island_1_3 = Island(Position(1, 3), 2)
        expected_island_2_0 = Island(Position(2, 0), 2)
        expected_island_2_1 = Island(Position(2, 1), 2)
        expected_island_2_2 = Island(Position(2, 2), 0)
        expected_island_2_3 = Island(Position(2, 3), 0)

        expected_island_0_0.set_bridge(Position(0, 1), 1)
        expected_island_0_0.set_bridge(Position(1, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 2), 1)
        expected_island_0_2.set_bridge(Position(0, 3), 1)
        expected_island_0_2.set_bridge(Position(0, 1), 1)
        expected_island_0_3.set_bridge(Position(0, 2), 1)
        expected_island_0_3.set_bridge(Position(1, 3), 1)
        expected_island_1_0.set_bridge(Position(0, 0), 1)
        expected_island_1_0.set_bridge(Position(2, 0), 1)
        expected_island_1_1.set_bridge(Position(1, 2), 1)
        expected_island_1_1.set_bridge(Position(2, 1), 1)
        expected_island_1_2.set_bridge(Position(1, 1), 1)
        expected_island_1_2.set_bridge(Position(1, 3), 1)
        expected_island_1_3.set_bridge(Position(1, 2), 1)
        expected_island_1_3.set_bridge(Position(0, 3), 1)
        expected_island_2_0.set_bridge(Position(2, 1), 1)
        expected_island_2_0.set_bridge(Position(1, 0), 1)
        expected_island_2_1.set_bridge(Position(1, 1), 1)
        expected_island_2_1.set_bridge(Position(2, 0), 1)

        expected_solution = Grid([
            [expected_island_0_0, expected_island_0_1, expected_island_0_2, expected_island_0_3],
            [expected_island_1_0, expected_island_1_1, expected_island_1_2, expected_island_1_3],
            [expected_island_2_0, expected_island_2_1, expected_island_2_2, expected_island_2_3]
        ])

        self.assertEqual(expected_solution, solution)

        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6(self):
        grid = Grid([
            [' ', 'b', ' ', ' ', 'w', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w', 'b', 'w', ' ', 'b'],
            [' ', ' ', ' ', ' ', ' ', 'b'],
            [' ', ' ', ' ', ' ', ' ', ' '],
            ['b', ' ', ' ', ' ', 'w', ' ']
        ])

        game = MasyuGame(grid)
        solution = game.get_solution()

        expected_island_0_0 = Island(Position(0, 0), 0)
        expected_island_0_1 = Island(Position(0, 1), 2)
        expected_island_0_2 = Island(Position(0, 2), 2)
        expected_island_0_3 = Island(Position(0, 3), 2)
        expected_island_0_4 = Island(Position(0, 4), 2)
        expected_island_0_5 = Island(Position(0, 5), 2)
        expected_island_1_0 = Island(Position(1, 0), 0)
        expected_island_1_1 = Island(Position(1, 1), 2)
        expected_island_1_2 = Island(Position(1, 2), 0)
        expected_island_1_3 = Island(Position(1, 3), 0)
        expected_island_1_4 = Island(Position(1, 4), 0)
        expected_island_1_5 = Island(Position(1, 5), 2)
        expected_island_2_0 = Island(Position(2, 0), 0)
        expected_island_2_1 = Island(Position(2, 1), 2)
        expected_island_2_2 = Island(Position(2, 2), 2)
        expected_island_2_3 = Island(Position(2, 3), 2)
        expected_island_2_4 = Island(Position(2, 4), 2)
        expected_island_2_5 = Island(Position(2, 5), 2)
        expected_island_3_0 = Island(Position(3, 0), 2)
        expected_island_3_1 = Island(Position(3, 1), 2)
        expected_island_3_2 = Island(Position(3, 2), 2)
        expected_island_3_3 = Island(Position(3, 3), 2)
        expected_island_3_4 = Island(Position(3, 4), 2)
        expected_island_3_5 = Island(Position(3, 5), 2)
        expected_island_4_0 = Island(Position(4, 0), 2)
        expected_island_4_1 = Island(Position(4, 1), 0)
        expected_island_4_2 = Island(Position(4, 2), 2)
        expected_island_4_3 = Island(Position(4, 3), 2)
        expected_island_4_4 = Island(Position(4, 4), 0)
        expected_island_4_5 = Island(Position(4, 5), 2)
        expected_island_5_0 = Island(Position(5, 0), 2)
        expected_island_5_1 = Island(Position(5, 1), 2)
        expected_island_5_2 = Island(Position(5, 2), 2)
        expected_island_5_3 = Island(Position(5, 3), 2)
        expected_island_5_4 = Island(Position(5, 4), 2)
        expected_island_5_5 = Island(Position(5, 5), 2)

        expected_island_0_1.set_bridge(Position(0, 2), 1)
        expected_island_0_1.set_bridge(Position(1, 1), 1)
        expected_island_0_2.set_bridge(Position(0, 1), 1)
        expected_island_0_2.set_bridge(Position(0, 3), 1)
        expected_island_0_3.set_bridge(Position(0, 2), 1)
        expected_island_0_3.set_bridge(Position(0, 4), 1)
        expected_island_0_4.set_bridge(Position(0, 5), 1)
        expected_island_0_4.set_bridge(Position(0, 3), 1)
        expected_island_0_5.set_bridge(Position(0, 4), 1)
        expected_island_0_5.set_bridge(Position(1, 5), 1)
        expected_island_1_1.set_bridge(Position(0, 1), 1)
        expected_island_1_1.set_bridge(Position(2, 1), 1)
        expected_island_1_5.set_bridge(Position(0, 5), 1)
        expected_island_1_5.set_bridge(Position(2, 5), 1)
        expected_island_2_1.set_bridge(Position(1, 1), 1)
        expected_island_2_1.set_bridge(Position(3, 1), 1)
        expected_island_2_2.set_bridge(Position(2, 3), 1)
        expected_island_2_2.set_bridge(Position(3, 2), 1)
        expected_island_2_3.set_bridge(Position(2, 2), 1)
        expected_island_2_3.set_bridge(Position(2, 4), 1)
        expected_island_2_4.set_bridge(Position(2, 5), 1)
        expected_island_2_4.set_bridge(Position(2, 3), 1)
        expected_island_2_5.set_bridge(Position(2, 4), 1)
        expected_island_2_5.set_bridge(Position(1, 5), 1)
        expected_island_3_0.set_bridge(Position(4, 0), 1)
        expected_island_3_0.set_bridge(Position(3, 1), 1)
        expected_island_3_1.set_bridge(Position(3, 0), 1)
        expected_island_3_1.set_bridge(Position(2, 1), 1)
        expected_island_3_2.set_bridge(Position(2, 2), 1)
        expected_island_3_2.set_bridge(Position(4, 2), 1)
        expected_island_3_3.set_bridge(Position(4, 3), 1)
        expected_island_3_3.set_bridge(Position(3, 4), 1)
        expected_island_3_4.set_bridge(Position(3, 3), 1)
        expected_island_3_4.set_bridge(Position(3, 5), 1)
        expected_island_3_5.set_bridge(Position(3, 4), 1)
        expected_island_3_5.set_bridge(Position(4, 5), 1)
        expected_island_4_0.set_bridge(Position(5, 0), 1)
        expected_island_4_0.set_bridge(Position(3, 0), 1)
        expected_island_4_2.set_bridge(Position(3, 2), 1)
        expected_island_4_2.set_bridge(Position(4, 3), 1)
        expected_island_4_3.set_bridge(Position(4, 2), 1)
        expected_island_4_3.set_bridge(Position(3, 3), 1)
        expected_island_4_5.set_bridge(Position(3, 5), 1)
        expected_island_4_5.set_bridge(Position(5, 5), 1)
        expected_island_5_0.set_bridge(Position(4, 0), 1)
        expected_island_5_0.set_bridge(Position(5, 1), 1)
        expected_island_5_1.set_bridge(Position(5, 0), 1)
        expected_island_5_1.set_bridge(Position(5, 2), 1)
        expected_island_5_2.set_bridge(Position(5, 1), 1)
        expected_island_5_2.set_bridge(Position(5, 3), 1)
        expected_island_5_3.set_bridge(Position(5, 2), 1)
        expected_island_5_3.set_bridge(Position(5, 4), 1)
        expected_island_5_4.set_bridge(Position(5, 5), 1)
        expected_island_5_4.set_bridge(Position(5, 3), 1)
        expected_island_5_5.set_bridge(Position(5, 4), 1)
        expected_island_5_5.set_bridge(Position(4, 5), 1)

        expected_solution = Grid([
            [expected_island_0_0, expected_island_0_1, expected_island_0_2, expected_island_0_3, expected_island_0_4, expected_island_0_5],
            [expected_island_1_0, expected_island_1_1, expected_island_1_2, expected_island_1_3, expected_island_1_4, expected_island_1_5],
            [expected_island_2_0, expected_island_2_1, expected_island_2_2, expected_island_2_3, expected_island_2_4, expected_island_2_5],
            [expected_island_3_0, expected_island_3_1, expected_island_3_2, expected_island_3_3, expected_island_3_4, expected_island_3_5],
            [expected_island_4_0, expected_island_4_1, expected_island_4_2, expected_island_4_3, expected_island_4_4, expected_island_4_5],
            [expected_island_5_0, expected_island_5_1, expected_island_5_2, expected_island_5_3, expected_island_5_4, expected_island_5_5]
        ])

        self.assertEqual(expected_solution, solution)

        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8(self):
        grid = Grid([
            ['b', 'w', ' ', 'w', ' ', ' ', 'w', ' '],
            ['w', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', ' '],
            [' ', 'w', 'w', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'b', 'w', 'w', ' ', 'w'],
            [' ', ' ', 'w', ' ', ' ', ' ', ' ', ' '],
            ['b', 'w', ' ', ' ', 'w', 'w', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w', ' ', 'w', 'b']
        ])

        game = MasyuGame(grid)
        solution = game.get_solution()

        ei_0_0 = Island(Position(0, 0), 2, {Position(0, 1): 1, Position(1, 0): 1})
        ei_0_1 = Island(Position(0, 1), 2, {Position(0, 0): 1, Position(0, 2): 1})
        ei_0_2 = Island(Position(0, 2), 2, {Position(0, 1): 1, Position(0, 3): 1})
        ei_0_3 = Island(Position(0, 3), 2, {Position(0, 2): 1, Position(0, 4): 1})
        ei_0_4 = Island(Position(0, 4), 2, {Position(0, 3): 1, Position(1, 4): 1})
        ei_0_5 = Island(Position(0, 5), 2, {Position(0, 6): 1, Position(1, 5): 1})
        ei_0_6 = Island(Position(0, 6), 2, {Position(0, 5): 1, Position(0, 7): 1})
        ei_0_7 = Island(Position(0, 7), 2, {Position(0, 6): 1, Position(1, 7): 1})
        ei_1_0 = Island(Position(1, 0), 2, {Position(0, 0): 1, Position(2, 0): 1})
        ei_1_1 = Island(Position(1, 1), 0)
        ei_1_2 = Island(Position(1, 2), 0)
        ei_1_3 = Island(Position(1, 3), 0)
        ei_1_4 = Island(Position(1, 4), 2, {Position(0, 4): 1, Position(2, 4): 1})
        ei_1_5 = Island(Position(1, 5), 2, {Position(0, 5): 1, Position(2, 5): 1})
        ei_1_6 = Island(Position(1, 6), 0)
        ei_1_7 = Island(Position(1, 7), 2, {Position(0, 7): 1, Position(2, 7): 1})
        ei_2_0 = Island(Position(2, 0), 2, {Position(1, 0): 1, Position(2, 1): 1})
        ei_2_1 = Island(Position(2, 1), 2, {Position(2, 0): 1, Position(3, 1): 1})
        ei_2_2 = Island(Position(2, 2), 2, {Position(2, 3): 1, Position(3, 2): 1})
        ei_2_3 = Island(Position(2, 3), 2, {Position(2, 2): 1, Position(3, 3): 1})
        ei_2_4 = Island(Position(2, 4), 2, {Position(1, 4): 1, Position(3, 4): 1})
        ei_2_5 = Island(Position(2, 5), 2, {Position(1, 5): 1, Position(3, 5): 1})
        ei_2_6 = Island(Position(2, 6), 2, {Position(2, 7): 1, Position(3, 6): 1})
        ei_2_7 = Island(Position(2, 7), 2, {Position(2, 6): 1, Position(1, 7): 1})
        ei_3_0 = Island(Position(3, 0), 0)
        ei_3_1 = Island(Position(3, 1), 2, {Position(2, 1): 1, Position(4, 1): 1})
        ei_3_2 = Island(Position(3, 2), 2, {Position(2, 2): 1, Position(4, 2): 1})
        ei_3_3 = Island(Position(3, 3), 2, {Position(2, 3): 1, Position(4, 3): 1})
        ei_3_4 = Island(Position(3, 4), 2, {Position(2, 4): 1, Position(3, 5): 1})
        ei_3_5 = Island(Position(3, 5), 2, {Position(2, 5): 1, Position(3, 4): 1})
        ei_3_6 = Island(Position(3, 6), 2, {Position(2, 6): 1, Position(3, 7): 1})
        ei_3_7 = Island(Position(3, 7), 2, {Position(3, 6): 1, Position(4, 7): 1})
        ei_4_0 = Island(Position(4, 0), 2, {Position(4, 1): 1, Position(5, 0): 1})
        ei_4_1 = Island(Position(4, 1), 2, {Position(3, 1): 1, Position(4, 0): 1})
        ei_4_2 = Island(Position(4, 2), 2, {Position(3, 2): 1, Position(5, 2): 1})
        ei_4_3 = Island(Position(4, 3), 2, {Position(3, 3): 1, Position(4, 4): 1})
        ei_4_4 = Island(Position(4, 4), 2, {Position(4, 3): 1, Position(4, 5): 1})
        ei_4_5 = Island(Position(4, 5), 2, {Position(4, 4): 1, Position(4, 6): 1})
        ei_4_6 = Island(Position(4, 6), 2, {Position(4, 5): 1, Position(5, 6): 1})
        ei_4_7 = Island(Position(4, 7), 2, {Position(3, 7): 1, Position(5, 7): 1})
        ei_5_0 = Island(Position(5, 0), 2, {Position(4, 0): 1, Position(6, 0): 1})
        ei_5_1 = Island(Position(5, 1), 0)
        ei_5_2 = Island(Position(5, 2), 2, {Position(4, 2): 1, Position(6, 2): 1})
        ei_5_3 = Island(Position(5, 3), 0)
        ei_5_4 = Island(Position(5, 4), 0)
        ei_5_5 = Island(Position(5, 5), 0)
        ei_5_6 = Island(Position(5, 6), 2, {Position(4, 6): 1, Position(6, 6): 1})
        ei_5_7 = Island(Position(5, 7), 2, {Position(4, 7): 1, Position(6, 7): 1})
        ei_6_0 = Island(Position(6, 0), 2, {Position(5, 0): 1, Position(6, 1): 1})
        ei_6_1 = Island(Position(6, 1), 2, {Position(6, 0): 1, Position(6, 2): 1})
        ei_6_2 = Island(Position(6, 2), 2, {Position(5, 2): 1, Position(6, 1): 1})
        ei_6_3 = Island(Position(6, 3), 2, {Position(6, 4): 1, Position(7, 3): 1})
        ei_6_4 = Island(Position(6, 4), 2, {Position(6, 3): 1, Position(6, 5): 1})
        ei_6_5 = Island(Position(6, 5), 2, {Position(6, 4): 1, Position(6, 6): 1})
        ei_6_6 = Island(Position(6, 6), 2, {Position(6, 5): 1, Position(5, 6): 1})
        ei_6_7 = Island(Position(6, 7), 2, {Position(5, 7): 1, Position(7, 7): 1})
        ei_7_0 = Island(Position(7, 0), 0)
        ei_7_1 = Island(Position(7, 1), 0)
        ei_7_2 = Island(Position(7, 2), 0)
        ei_7_3 = Island(Position(7, 3), 2, {Position(6, 3): 1, Position(7, 4): 1})
        ei_7_4 = Island(Position(7, 4), 2, {Position(7, 3): 1, Position(7, 5): 1})
        ei_7_5 = Island(Position(7, 5), 2, {Position(7, 4): 1, Position(7, 6): 1})
        ei_7_6 = Island(Position(7, 6), 2, {Position(7, 5): 1, Position(7, 7): 1})
        ei_7_7 = Island(Position(7, 7), 2, {Position(7, 6): 1, Position(6, 7): 1})

        expected_solution = Grid([
            [ei_0_0, ei_0_1, ei_0_2, ei_0_3, ei_0_4, ei_0_5, ei_0_6, ei_0_7],
            [ei_1_0, ei_1_1, ei_1_2, ei_1_3, ei_1_4, ei_1_5, ei_1_6, ei_1_7],
            [ei_2_0, ei_2_1, ei_2_2, ei_2_3, ei_2_4, ei_2_5, ei_2_6, ei_2_7],
            [ei_3_0, ei_3_1, ei_3_2, ei_3_3, ei_3_4, ei_3_5, ei_3_6, ei_3_7],
            [ei_4_0, ei_4_1, ei_4_2, ei_4_3, ei_4_4, ei_4_5, ei_4_6, ei_4_7],
            [ei_5_0, ei_5_1, ei_5_2, ei_5_3, ei_5_4, ei_5_5, ei_5_6, ei_5_7],
            [ei_6_0, ei_6_1, ei_6_2, ei_6_3, ei_6_4, ei_6_5, ei_6_6, ei_6_7],
            [ei_7_0, ei_7_1, ei_7_2, ei_7_3, ei_7_4, ei_7_5, ei_7_6, ei_7_7]
        ])

        self.assertEqual(expected_solution, solution)

        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_2(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b'],
            ['w', ' ', 'b', ' ', 'b', ' ', ' ', ' '],
            ['w', ' ', ' ', ' ', ' ', 'w', ' ', ' '],
            [' ', 'w', ' ', ' ', ' ', ' ', 'w', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['b', ' ', ' ', 'b', 'b', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w', ' ', 'w', ' ', ' ', ' ', 'b']
        ])

        game = MasyuGame(grid)
        solution = game.get_solution()

        ei_0_0 = Island(Position(0, 0), 2, {Position(0, 1): 1, Position(1, 0): 1})
        ei_0_1 = Island(Position(0, 1), 2, {Position(0, 0): 1, Position(0, 2): 1})
        ei_0_2 = Island(Position(0, 2), 2, {Position(0, 1): 1, Position(0, 3): 1})
        ei_0_3 = Island(Position(0, 3), 2, {Position(0, 2): 1, Position(0, 4): 1})
        ei_0_4 = Island(Position(0, 4), 2, {Position(0, 3): 1, Position(0, 5): 1})
        ei_0_5 = Island(Position(0, 5), 2, {Position(0, 4): 1, Position(0, 6): 1})
        ei_0_6 = Island(Position(0, 6), 2, {Position(0, 5): 1, Position(0, 7): 1})
        ei_0_7 = Island(Position(0, 7), 2, {Position(0, 6): 1, Position(1, 7): 1})
        ei_1_0 = Island(Position(1, 0), 2, {Position(0, 0): 1, Position(2, 0): 1})
        ei_1_1 = Island(Position(1, 1), 0)
        ei_1_2 = Island(Position(1, 2), 2, {Position(1, 3): 1, Position(2, 2): 1})
        ei_1_3 = Island(Position(1, 3), 2, {Position(1, 2): 1, Position(1, 4): 1})
        ei_1_4 = Island(Position(1, 4), 2, {Position(1, 3): 1, Position(2, 4): 1})
        ei_1_5 = Island(Position(1, 5), 2, {Position(1, 6): 1, Position(2, 5): 1})
        ei_1_6 = Island(Position(1, 6), 2, {Position(1, 5): 1, Position(2, 6): 1})
        ei_1_7 = Island(Position(1, 7), 2, {Position(0, 7): 1, Position(2, 7): 1})
        ei_2_0 = Island(Position(2, 0), 2, {Position(1, 0): 1, Position(3, 0): 1})
        ei_2_1 = Island(Position(2, 1), 0)
        ei_2_2 = Island(Position(2, 2), 2, {Position(1, 2): 1, Position(3, 2): 1})
        ei_2_3 = Island(Position(2, 3), 0)
        ei_2_4 = Island(Position(2, 4), 2, {Position(1, 4): 1, Position(3, 4): 1})
        ei_2_5 = Island(Position(2, 5), 2, {Position(1, 5): 1, Position(3, 5): 1})
        ei_2_6 = Island(Position(2, 6), 2, {Position(1, 6): 1, Position(2, 7): 1})
        ei_2_7 = Island(Position(2, 7), 2, {Position(1, 7): 1, Position(2, 6): 1})
        ei_3_0 = Island(Position(3, 0), 2, {Position(2, 0): 1, Position(3, 1): 1})
        ei_3_1 = Island(Position(3, 1), 2, {Position(3, 0): 1, Position(3, 2): 1})
        ei_3_2 = Island(Position(3, 2), 2, {Position(2, 2): 1, Position(3, 1): 1})
        ei_3_3 = Island(Position(3, 3), 2, {Position(3, 4): 1, Position(4, 3): 1})
        ei_3_4 = Island(Position(3, 4), 2, {Position(2, 4): 1, Position(3, 3): 1})
        ei_3_5 = Island(Position(3, 5), 2, {Position(2, 5): 1, Position(3, 6): 1})
        ei_3_6 = Island(Position(3, 6), 2, {Position(3, 5): 1, Position(3, 7): 1})
        ei_3_7 = Island(Position(3, 7), 2, {Position(3, 6): 1, Position(4, 7): 1})
        ei_4_0 = Island(Position(4, 0), 0)
        ei_4_1 = Island(Position(4, 1), 0)
        ei_4_2 = Island(Position(4, 2), 0)
        ei_4_3 = Island(Position(4, 3), 2, {Position(3, 3): 1, Position(5, 3): 1})
        ei_4_4 = Island(Position(4, 4), 0)
        ei_4_5 = Island(Position(4, 5), 0)
        ei_4_6 = Island(Position(4, 6), 0)
        ei_4_7 = Island(Position(4, 7), 2, {Position(3, 7): 1, Position(5, 7): 1})
        ei_5_0 = Island(Position(5, 0), 2, {Position(6, 0): 1, Position(5, 1): 1})
        ei_5_1 = Island(Position(5, 1), 2, {Position(5, 0): 1, Position(5, 2): 1})
        ei_5_2 = Island(Position(5, 2), 2, {Position(5, 1): 1, Position(5, 3): 1})
        ei_5_3 = Island(Position(5, 3), 2, {Position(4, 3): 1, Position(5, 2): 1})
        ei_5_4 = Island(Position(5, 4), 2, {Position(5, 5): 1, Position(6, 4): 1})
        ei_5_5 = Island(Position(5, 5), 2, {Position(5, 4): 1, Position(5, 6): 1})
        ei_5_6 = Island(Position(5, 6), 2, {Position(5, 5): 1, Position(6, 6): 1})
        ei_5_7 = Island(Position(5, 7), 2, {Position(4, 7): 1, Position(6, 7): 1})
        ei_6_0 = Island(Position(6, 0), 2, {Position(5, 0): 1, Position(7, 0): 1})
        ei_6_1 = Island(Position(6, 1), 0)
        ei_6_2 = Island(Position(6, 2), 0)
        ei_6_3 = Island(Position(6, 3), 0)
        ei_6_4 = Island(Position(6, 4), 2, {Position(5, 4): 1, Position(7, 4): 1})
        ei_6_5 = Island(Position(6, 5), 2, {Position(7, 5): 1, Position(6, 6): 1})
        ei_6_6 = Island(Position(6, 6), 2, {Position(6, 5): 1, Position(5, 6): 1})
        ei_6_7 = Island(Position(6, 7), 2, {Position(5, 7): 1, Position(7, 7): 1})
        ei_7_0 = Island(Position(7, 0), 2, {Position(6, 0): 1, Position(7, 1): 1})
        ei_7_1 = Island(Position(7, 1), 2, {Position(7, 0): 1, Position(7, 2): 1})
        ei_7_2 = Island(Position(7, 2), 2, {Position(7, 1): 1, Position(7, 3): 1})
        ei_7_3 = Island(Position(7, 3), 2, {Position(7, 2): 1, Position(7, 4): 1})
        ei_7_4 = Island(Position(7, 4), 2, {Position(7, 3): 1, Position(6, 4): 1})
        ei_7_5 = Island(Position(7, 5), 2, {Position(6, 5): 1, Position(7, 6): 1})
        ei_7_6 = Island(Position(7, 6), 2, {Position(7, 5): 1, Position(7, 7): 1})
        ei_7_7 = Island(Position(7, 7), 2, {Position(7, 6): 1, Position(6, 7): 1})

        expected_solution = Grid([
            [ei_0_0, ei_0_1, ei_0_2, ei_0_3, ei_0_4, ei_0_5, ei_0_6, ei_0_7],
            [ei_1_0, ei_1_1, ei_1_2, ei_1_3, ei_1_4, ei_1_5, ei_1_6, ei_1_7],
            [ei_2_0, ei_2_1, ei_2_2, ei_2_3, ei_2_4, ei_2_5, ei_2_6, ei_2_7],
            [ei_3_0, ei_3_1, ei_3_2, ei_3_3, ei_3_4, ei_3_5, ei_3_6, ei_3_7],
            [ei_4_0, ei_4_1, ei_4_2, ei_4_3, ei_4_4, ei_4_5, ei_4_6, ei_4_7],
            [ei_5_0, ei_5_1, ei_5_2, ei_5_3, ei_5_4, ei_5_5, ei_5_6, ei_5_7],
            [ei_6_0, ei_6_1, ei_6_2, ei_6_3, ei_6_4, ei_6_5, ei_6_6, ei_6_7],
            [ei_7_0, ei_7_1, ei_7_2, ei_7_3, ei_7_4, ei_7_5, ei_7_6, ei_7_7]
        ])

        self.assertEqual(expected_solution, solution)

        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)