from unittest import TestCase

from Utils.Island import Island
from Utils.IslandsGrid import IslandGrid
from Utils.Position import Position


class IslandGridTest(TestCase):
    def test_empty(self):
        island_grid = IslandGrid.empty()
        island_grid_repr = repr(island_grid)
        expected_repr = 'IslandGrid.empty()'
        self.assertEqual(expected_repr, island_grid_repr)

    def test_11(self):
        island00 = Island(Position(0, 0), 1)
        island01 = Island(Position(0, 1), 1)

        island_matrix = [[island00, island01]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(0, 1), 1)
        island01.set_bridge(Position(0, 0), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = ' ╶──╴ '
        self.assertEqual(expected_repr, island_grid_repr)

    def test_121(self):
        island00 = Island(Position(0, 0), 1)
        island01 = Island(Position(0, 1), 2)
        island02 = Island(Position(0, 2), 1)

        island_matrix = [[island00, island01, island02]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(0, 1), 1)
        island01.set_bridge(Position(0, 0), 1)
        island01.set_bridge(Position(0, 2), 1)
        island02.set_bridge(Position(0, 1), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = ' ╶─────╴ '
        self.assertEqual(expected_repr, island_grid_repr)

    def test_1_1(self):
        island00 = Island(Position(0, 0), 1)
        island10 = Island(Position(1, 0), 1)

        island_matrix = [[island00], [island10]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(1, 0), 1)
        island10.set_bridge(Position(0, 0), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = (
            ' ╷ \n'
            ' ╵ '
        )
        self.assertEqual(expected_repr, island_grid_repr)

    def test_1_2_1(self):
        island00 = Island(Position(0, 0), 1)
        island10 = Island(Position(1, 0), 2)
        island20 = Island(Position(2, 0), 1)

        island_matrix = [[island00], [island10], [island20]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(1, 0), 1)
        island10.set_bridge(Position(0, 0), 1)
        island10.set_bridge(Position(2, 0), 1)
        island20.set_bridge(Position(1, 0), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = (
            ' ╷ \n'
            ' │ \n'
            ' ╵ '
        )
        self.assertEqual(expected_repr, island_grid_repr)

    def test_22_22(self):
        island00 = Island(Position(0, 0), 2)
        island01 = Island(Position(0, 1), 2)
        island10 = Island(Position(1, 0), 2)
        island11 = Island(Position(1, 1), 2)

        island_matrix = [[island00, island01], [island10, island11]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(1, 0), 1)
        island00.set_bridge(Position(0, 1), 1)
        island10.set_bridge(Position(0, 0), 1)
        island10.set_bridge(Position(1, 1), 1)
        island01.set_bridge(Position(1, 1), 1)
        island01.set_bridge(Position(0, 0), 1)
        island11.set_bridge(Position(0, 1), 1)
        island11.set_bridge(Position(1, 0), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = (
            ' ┌──┐ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_repr, island_grid_repr)

    def test_110(self):
        island00 = Island(Position(0, 0), 1)
        island01 = Island(Position(0, 1), 1)
        island02 = Island(Position(0, 2), 0)

        island_matrix = [[island00, island01, island02]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(0, 1), 1)
        island01.set_bridge(Position(0, 0), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = ' ╶──╴    '

        self.assertEqual(expected_repr, island_grid_repr)

    def test_11None11(self):
        island00 = Island(Position(0, 0), 1)
        island01 = Island(Position(0, 1), 1)
        none_island02 = None
        island03 = Island(Position(0, 3), 1)
        island04 = Island(Position(0, 4), 1)

        island_matrix = [[island00, island01, none_island02, island03, island04]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(0, 1), 1)
        island01.set_bridge(Position(0, 0), 1)
        island03.set_bridge(Position(0, 4), 1)
        island04.set_bridge(Position(0, 3), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = ' ╶──╴     ╶──╴ '

        self.assertEqual(expected_repr, island_grid_repr)

    def test_11011(self):
        island00 = Island(Position(0, 0), 1)
        island01 = Island(Position(0, 1), 1)
        island02 = Island(Position(0, 2), 0)
        island03 = Island(Position(0, 3), 1)
        island04 = Island(Position(0, 4), 1)

        island_matrix = [[island00, island01, island02, island03, island04]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(0, 1), 1)
        island01.set_bridge(Position(0, 0), 1)
        island03.set_bridge(Position(0, 4), 1)
        island04.set_bridge(Position(0, 3), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = ' ╶──╴     ╶──╴ '

        self.assertEqual(expected_repr, island_grid_repr)

    def test_12None21(self):
        island00 = Island(Position(0, 0), 1)
        island01 = Island(Position(0, 1), 2)
        none_island02 = None
        island03 = Island(Position(0, 3), 2)
        island04 = Island(Position(0, 4), 1)

        island_matrix = [[island00, island01, none_island02, island03, island04]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(0, 1), 1)
        island01.set_bridge(Position(0, 0), 1)
        island01.set_bridge(Position(0, 3), 1)
        island03.set_bridge(Position(0, 4), 1)
        island03.set_bridge(Position(0, 1), 1)
        island04.set_bridge(Position(0, 3), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = ' ╶───────────╴ '

        self.assertEqual(expected_repr, island_grid_repr)

    def test_12NoneNone21(self):
        island00 = Island(Position(0, 0), 1)
        island01 = Island(Position(0, 1), 2)
        none_island02 = None
        none_island03 = None
        island04 = Island(Position(0, 4), 2)
        island05 = Island(Position(0, 5), 1)

        island_matrix = [[island00, island01, none_island02, none_island03, island04, island05]]
        island_grid = IslandGrid(island_matrix)
        island00.set_bridge(Position(0, 1), 1)
        island01.set_bridge(Position(0, 0), 1)
        island01.set_bridge(Position(0, 4), 1)
        island04.set_bridge(Position(0, 5), 1)
        island04.set_bridge(Position(0, 1), 1)
        island05.set_bridge(Position(0, 4), 1)

        island_grid_repr = repr(island_grid)
        expected_repr = ' ╶──────────────╴ '

        self.assertEqual(expected_repr, island_grid_repr)
