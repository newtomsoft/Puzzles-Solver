import unittest
from unittest import TestCase

from Puzzles.Hashi.Island import Island
from Utils.Direction import Direction
from Utils.Position import Position


class IslandTest(TestCase):
    def setUp(self):
        Island._islands = {}

    def test_island_links_number(self):
        for i in range(1, 9):
            island = Island(Position(0, i), i)
            self.assertEqual(i, island.links_number)

    def test_island_links_number_exception(self):
        with self.assertRaises(ValueError) as context:
            Island(Position(0, 0), 0)
        self.assertEqual("Links number must be between 1 and 8", str(context.exception))
        with self.assertRaises(ValueError) as context:
            Island(Position(0, 0), 9)
        self.assertEqual("Links number must be between 1 and 8", str(context.exception))

    def test_compute_possible_links_when_only_one_island_by_direction(self):
        island_0_1 = Island(Position(0, 1), 2)
        island_0_2 = Island(Position(0, 2), 2)
        island_1_0 = Island(Position(1, 0), 2)
        island_1_2 = Island(Position(1, 2), 2)
        island_2_1 = Island(Position(2, 1), 2)
        expected_island_0_1_direction_islands_ids_links_number = {Direction.RIGHT: (island_0_2.position, 0), Direction.DOWN: (island_2_1.position, 0)}
        self.assertEqual(expected_island_0_1_direction_islands_ids_links_number, island_0_1.direction_islands_links_number)
        expected_island_0_2_direction_islands_ids_links_number = {Direction.LEFT: (island_0_1.position, 0), Direction.DOWN: (island_1_2.position, 0)}
        self.assertEqual(expected_island_0_2_direction_islands_ids_links_number, island_0_2.direction_islands_links_number)
        expected_island_1_0_direction_islands_ids_links_number = {Direction.RIGHT: (island_1_2.position, 0)}
        self.assertEqual(expected_island_1_0_direction_islands_ids_links_number, island_1_0.direction_islands_links_number)
        expected_island_1_2_direction_islands_ids_links_number = {Direction.LEFT: (island_1_0.position, 0), Direction.UP: (island_0_2.position, 0)}
        self.assertEqual(expected_island_1_2_direction_islands_ids_links_number, island_1_2.direction_islands_links_number)
        expected_island_2_1_direction_islands_ids_links_number = {Direction.UP: (island_0_1.position, 0)}
        self.assertEqual(expected_island_2_1_direction_islands_ids_links_number, island_2_1.direction_islands_links_number)

    def test_compute_possible_links(self):
        island_0_0 = Island(Position(0, 0), 2)
        island_0_2 = Island(Position(0, 2), 2)
        island_0_6 = Island(Position(0, 6), 2)
        island_1_1 = Island(Position(1, 1), 2)
        island_1_4 = Island(Position(1, 4), 2)
        island_2_3 = Island(Position(2, 3), 2)
        island_2_5 = Island(Position(2, 5), 2)
        island_3_0 = Island(Position(3, 0), 2)
        island_3_4 = Island(Position(3, 4), 2)
        island_4_2 = Island(Position(4, 2), 2)
        island_4_5 = Island(Position(4, 5), 2)
        island_5_1 = Island(Position(5, 1), 2)
        island_5_6 = Island(Position(5, 6), 2)
        island_6_0 = Island(Position(6, 0), 2)
        island_6_5 = Island(Position(6, 5), 2)
        expected_island_0_0_direction_islands_ids_links_number = {Direction.RIGHT: (island_0_2.position, 0), Direction.DOWN: (island_3_0.position, 0)}
        self.assertEqual(expected_island_0_0_direction_islands_ids_links_number, island_0_0.direction_islands_links_number)
        expected_island_0_2_direction_islands_ids_links_number = {Direction.LEFT: (island_0_0.position, 0), Direction.DOWN: (island_4_2.position, 0), Direction.RIGHT: (island_0_6.position, 0)}
        self.assertEqual(expected_island_0_2_direction_islands_ids_links_number, island_0_2.direction_islands_links_number)
        expected_island_0_6_direction_islands_ids_links_number = {Direction.LEFT: (island_0_2.position, 0), Direction.DOWN: (island_5_6.position, 0)}
        self.assertEqual(expected_island_0_6_direction_islands_ids_links_number, island_0_6.direction_islands_links_number)
        expected_island_1_1_direction_islands_ids_links_number = {Direction.RIGHT: (island_1_4.position, 0), Direction.DOWN: (island_5_1.position, 0)}
        self.assertEqual(expected_island_1_1_direction_islands_ids_links_number, island_1_1.direction_islands_links_number)
        expected_island_1_4_direction_islands_ids_links_number = {Direction.LEFT: (island_1_1.position, 0), Direction.DOWN: (island_3_4.position, 0)}
        self.assertEqual(expected_island_1_4_direction_islands_ids_links_number, island_1_4.direction_islands_links_number)
        expected_island_2_3_direction_islands_ids_links_number = {Direction.RIGHT: (island_2_5.position, 0)}
        self.assertEqual(expected_island_2_3_direction_islands_ids_links_number, island_2_3.direction_islands_links_number)
        expected_island_2_5_direction_islands_ids_links_number = {Direction.LEFT: (island_2_3.position, 0), Direction.DOWN: (island_4_5.position, 0)}
        self.assertEqual(expected_island_2_5_direction_islands_ids_links_number, island_2_5.direction_islands_links_number)
        expected_island_3_0_direction_islands_ids_links_number = {Direction.RIGHT: (island_3_4.position, 0), Direction.UP: (island_0_0.position, 0), Direction.DOWN: (island_6_0.position, 0)}
        self.assertEqual(expected_island_3_0_direction_islands_ids_links_number, island_3_0.direction_islands_links_number)
        expected_island_3_4_direction_islands_ids_links_number = {Direction.LEFT: (island_3_0.position, 0), Direction.UP: (island_1_4.position, 0)}
        self.assertEqual(expected_island_3_4_direction_islands_ids_links_number, island_3_4.direction_islands_links_number)
        expected_island_4_2_direction_islands_ids_links_number = {Direction.RIGHT: (island_4_5.position, 0), Direction.UP: (island_0_2.position, 0)}
        self.assertEqual(expected_island_4_2_direction_islands_ids_links_number, island_4_2.direction_islands_links_number)
        expected_island_4_5_direction_islands_ids_links_number = {Direction.LEFT: (island_4_2.position, 0), Direction.UP: (island_2_5.position, 0), Direction.DOWN: (island_6_5.position, 0)}
        self.assertEqual(expected_island_4_5_direction_islands_ids_links_number, island_4_5.direction_islands_links_number)
        expected_island_5_1_direction_islands_ids_links_number = {Direction.RIGHT: (island_5_6.position, 0), Direction.UP: (island_1_1.position, 0)}
        self.assertEqual(expected_island_5_1_direction_islands_ids_links_number, island_5_1.direction_islands_links_number)
        expected_island_5_6_direction_islands_ids_links_number = {Direction.LEFT: (island_5_1.position, 0), Direction.UP: (island_0_6.position, 0)}
        self.assertEqual(expected_island_5_6_direction_islands_ids_links_number, island_5_6.direction_islands_links_number)
        expected_island_6_0_direction_islands_ids_links_number = {Direction.RIGHT: (island_6_5.position, 0), Direction.UP: (island_3_0.position, 0)}
        self.assertEqual(expected_island_6_0_direction_islands_ids_links_number, island_6_0.direction_islands_links_number)
        expected_island_6_5_direction_islands_ids_links_number = {Direction.LEFT: (island_6_0.position, 0), Direction.UP: (island_4_5.position, 0)}
        self.assertEqual(expected_island_6_5_direction_islands_ids_links_number, island_6_5.direction_islands_links_number)


if __name__ == '__main__':
    unittest.main()