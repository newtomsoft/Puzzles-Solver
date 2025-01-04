import unittest
from unittest import TestCase

from Puzzles.Hashi.Island import Island
from Utils.Position import Position


class IslandTest(TestCase):
    def setUp(self):
        Island._islands = {}

    def test_island_bridges(self):
        for i in range(1, 9):
            island = Island(Position(0, i), i)
            self.assertEqual(i, island.bridges)

    def test_island_bridges_exception(self):
        with self.assertRaises(ValueError) as context:
            Island(Position(0, 0), 0)
        self.assertEqual("Bridges must be between 1 and 8", str(context.exception))
        with self.assertRaises(ValueError) as context:
            Island(Position(0, 0), 9)
        self.assertEqual("Bridges must be between 1 and 8", str(context.exception))


if __name__ == '__main__':
    unittest.main()
