from unittest import TestCase

from Puzzles.Hashi.HashiGame import HashiGame
from Puzzles.Hashi.Island import Island
from Utils.Position import Position


class HashiGameTests(TestCase):
    def test(self):
        island_0_0 = Island(Position(0, 0), 1)
        island_0_1 = Island(Position(0, 1), 4)
        island_0_3 = Island(Position(0, 3), 3)
        island_1_2 = Island(Position(1, 2), 2)
        island_2_0 = Island(Position(2, 0), 1)
        island_2_2 = Island(Position(2, 2), 4)
        island_2_3 = Island(Position(2, 3), 4)
        island_3_1 = Island(Position(3, 1), 2)
        island_4_2 = Island(Position(4, 2), 1)
        island_5_0 = Island(Position(5, 0), 2)
        island_5_3 = Island(Position(5, 3), 2)
        islands = [island_0_0, island_0_1, island_0_3, island_1_2, island_2_0, island_2_2, island_2_3, island_3_1, island_4_2, island_5_0, island_5_3]
        game = HashiGame(islands)
        solution = game.get_solution()
