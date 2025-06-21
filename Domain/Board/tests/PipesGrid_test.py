from unittest import TestCase

from Domain.Board.Direction import Direction
from Domain.Board.Pipe import Pipe
from Domain.Board.PipesGrid import PipesGrid
from Domain.Board.Position import Position


class PipesGridTest(TestCase):
    def test_get_connected_positions_all_connected(self):
        pipe00 = Pipe.from_connection(frozenset([Direction.right()]))
        pipe01 = Pipe.from_connection(frozenset([Direction.down(), Direction.left()]))
        pipe10 = Pipe.from_connection(frozenset([Direction.right()]))
        pipe11 = Pipe.from_connection(frozenset([Direction.up(), Direction.left()]))

        pipes_matrix = [
            [pipe00, pipe01],
            [pipe10, pipe11],
        ]
        pipes_grid = PipesGrid(pipes_matrix)

        connected_positions, is_loop = pipes_grid.get_connected_positions_and_is_loop()

        expected_connected_positions = [
            {Position(0, 1), Position(1, 0), Position(1, 1), Position(0, 0)}
        ]
        self.assertEqual(expected_connected_positions, connected_positions)
        self.assertFalse(is_loop)

    def test_get_connected_positions_1_pipe_isolated(self):
        pipe00 = Pipe.from_connection(frozenset([Direction.right()]))
        pipe01 = Pipe.from_connection(frozenset([Direction.down(), Direction.left()]))
        pipe10 = Pipe.from_connection(frozenset([Direction.right()]))
        pipe11 = Pipe.from_connection(frozenset([Direction.up()]))

        pipes_matrix = [
            [pipe00, pipe01],
            [pipe10, pipe11],
        ]
        pipes_grid = PipesGrid(pipes_matrix)

        connected_positions, is_loop = pipes_grid.get_connected_positions_and_is_loop()

        expected_connected_positions = [
            {Position(0, 1), Position(1, 1), Position(0, 0)},
            {Position(1, 0)}
        ]
        self.assertEqual(expected_connected_positions, connected_positions)
        self.assertFalse(is_loop)

    def test_get_connected_positions_when_loop(self):
        pipe00 = Pipe.from_connection(frozenset([Direction.right()]))
        pipe01 = Pipe.from_connection(frozenset([Direction.down(), Direction.left(), Direction.right()]))
        pipe02 = Pipe.from_connection(frozenset([Direction.down(), Direction.left()]))
        pipe10 = Pipe.from_connection(frozenset([Direction.right()]))
        pipe11 = Pipe.from_connection(frozenset([Direction.up(), Direction.left(), Direction.right()]))
        pipe12 = Pipe.from_connection(frozenset([Direction.up(), Direction.left()]))

        pipes_matrix = [
            [pipe00, pipe01, pipe02],
            [pipe10, pipe11, pipe12],
        ]
        pipes_grid = PipesGrid(pipes_matrix)

        connected_positions, is_loop = pipes_grid.get_connected_positions_and_is_loop()

        expected_connected_positions = [
            {Position(0, 0), Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)}
        ]
        self.assertEqual(expected_connected_positions, connected_positions)
        self.assertTrue(is_loop)
