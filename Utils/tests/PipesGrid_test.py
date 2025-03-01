from unittest import TestCase

from Pipes.Pipe import Pipe
from Utils.PipesGrid import PipesGrid
from Utils.Position import Position


class PipesGridTest(TestCase):
    def test_get_connected_positions_all_connected(self):
        pipe00 = Pipe.from_connection(right=True)
        pipe01 = Pipe.from_connection(down=True, left=True)
        pipe10 = Pipe.from_connection(right=True)
        pipe11 = Pipe.from_connection(up=True, left=True)

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
        pipe00 = Pipe.from_connection(right=True)
        pipe01 = Pipe.from_connection(down=True, left=True)
        pipe10 = Pipe.from_connection(up=False, right=True)
        pipe11 = Pipe.from_connection(up=True)

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
        pipe00 = Pipe.from_connection(right=True)
        pipe01 = Pipe.from_connection(down=True, left=True, right=True)
        pipe02 = Pipe.from_connection(down=True, left=True)
        pipe10 = Pipe.from_connection(right=True)
        pipe11 = Pipe.from_connection(up=True, left=True, right=True)
        pipe12 = Pipe.from_connection(up=True, left=True)

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
