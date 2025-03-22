import unittest
from unittest import TestCase

from bitarray import bitarray

from Utils.Grid import Grid
from Utils.Position import Position
from Utils.colors import console_police_colors, console_back_ground_colors, remove_ansi_escape_sequences


class GridTest(TestCase):
    def setUp(self):
        self.grid_2x2 = Grid([
            ['1', '2'],
            ['3', '4']
        ])
        self.grid_3x3 = Grid([
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']
        ])
        self.grid_2x3 = Grid([
            ['1', '2', '3'],
            ['4', '5', '6']
        ])
        self.grid_3x2 = Grid([
            ['1', '2'],
            ['3', '4'],
            ['5', '6']
        ])
        self.grid_dfs = Grid([
            ['1', '1', '2', '3', '8'],
            ['8', '8', '2', '8', '8'],
            ['8', '3', '5', '5', '8'],
            ['8', '8', '8', '8', '8']
        ])
        self.grid_dfs_diagonal = Grid([
            ['1', '8', '1', '2', '2'],
            ['8', '1', '5', '9', '2'],
            ['1', '3', '1', '5', '9'],
            ['6', '6', '3', '9', '7']
        ])

        self.grid_dfs_diagonal_border = Grid([
            ['1', '5', '0', '5', '1'],
            ['5', '1', '3', '1', '5'],
            ['1', '9', '0', '9', '1'],
            ['9', '0', '3', '0', '9']
        ])

    def test_value_2x3(self):
        self.assertEqual('1', self.grid_2x3.value(0, 0))
        self.assertEqual('2', self.grid_2x3.value(0, 1))
        self.assertEqual('3', self.grid_2x3.value(0, 2))
        self.assertEqual('4', self.grid_2x3.value(1, 0))
        self.assertEqual('5', self.grid_2x3.value(1, 1))
        self.assertEqual('6', self.grid_2x3.value(1, 2))

    def test_depth_first_search_1(self):
        visited = self.grid_dfs._depth_first_search(Position(0, 0), '1', 'orthogonal')
        expected_visited = {Position(0, 0), Position(0, 1)}
        self.assertEqual(expected_visited, visited)

    def test_depth_first_search_2(self):
        visited = self.grid_dfs._depth_first_search(Position(0, 2), '2', 'orthogonal')
        expected_visited = {Position(0, 2), Position(1, 2)}
        self.assertEqual(expected_visited, visited)

    def test_depth_first_search_5(self):
        visited = self.grid_dfs._depth_first_search(Position(2, 2), '5', 'orthogonal')
        expected_visited = {Position(2, 2), Position(2, 3)}
        self.assertEqual(expected_visited, visited)

    def test_depth_first_search_8(self):
        visited = self.grid_dfs._depth_first_search(Position(1, 3), '8', 'orthogonal')
        expected_visited = {Position(1, 3), Position(0, 4), Position(1, 0), Position(1, 1), Position(1, 4), Position(2, 0), Position(2, 4), Position(3, 0), Position(3, 1), Position(3, 2),
                            Position(3, 3), Position(3, 4)}
        self.assertEqual(expected_visited, visited)

    def test_depth_first_search_3_by_0_3(self):
        visited = self.grid_dfs._depth_first_search(Position(0, 3), '3', 'orthogonal')
        expected_visited = {Position(0, 3)}
        self.assertEqual(expected_visited, visited)

    def test_depth_first_search_3_by_2_0(self):
        visited = self.grid_dfs._depth_first_search(Position(2, 1), '3', 'orthogonal')
        expected_visited = {Position(2, 1)}
        self.assertEqual(expected_visited, visited)

    def test_all_cells_connected_1(self):
        self.assertTrue(self.grid_dfs.are_cells_connected('1', 'orthogonal'))

    def test_all_cells_connected_2(self):
        self.assertTrue(self.grid_dfs.are_cells_connected('2', 'orthogonal'))

    def test_all_cells_connected_5(self):
        self.assertFalse(self.grid_dfs.are_cells_connected('3', 'orthogonal'))

    def test_all_cells_connected_8(self):
        self.assertTrue(self.grid_dfs.are_cells_connected('8', 'orthogonal'))

    def test_all_cells_connected_9(self):
        self.assertFalse(self.grid_dfs.are_cells_connected('9', 'orthogonal'))

    def test_all_cells_connected_10(self):
        self.assertFalse(self.grid_dfs.are_cells_connected('10', 'orthogonal'))

    def test_all_cells_connected_diagonally_0(self):
        self.assertFalse(self.grid_dfs.are_cells_connected('0', 'diagonal'))

    def test_all_cells_connected_diagonally_1(self):
        self.assertTrue(self.grid_dfs_diagonal.are_cells_connected('1', 'diagonal'))

    def test_all_cells_connected_diagonally_2(self):
        self.assertFalse(self.grid_dfs_diagonal.are_cells_connected('2', 'diagonal'))

    def test_all_cells_connected_diagonally_3(self):
        self.assertTrue(self.grid_dfs_diagonal.are_cells_connected('3', 'diagonal'))

    def test_all_cells_connected_diagonally_5(self):
        self.assertTrue(self.grid_dfs_diagonal.are_cells_connected('5', 'diagonal'))

    def test_all_cells_connected_diagonally_6(self):
        self.assertFalse(self.grid_dfs_diagonal.are_cells_connected('6', 'diagonal'))

    def test_all_cells_connected_diagonally_7(self):
        self.assertTrue(self.grid_dfs_diagonal.are_cells_connected('7', 'diagonal'))

    def test_all_cells_connected_diagonally_8(self):
        self.assertTrue(self.grid_dfs_diagonal.are_cells_connected('8', 'diagonal'))

    def test_all_cells_connected_diagonally_9(self):
        self.assertTrue(self.grid_dfs_diagonal.are_cells_connected('9', 'diagonal'))

    def test_min_2_connected_cells_touch_border_0_0(self):
        self.assertTrue(self.grid_dfs.are_min_2_connected_cells_touch_border(Position(0, 0), 'orthogonal')[0])

    def test_min_2_connected_cells_touch_border_0_2(self):
        self.assertFalse(self.grid_dfs.are_min_2_connected_cells_touch_border(Position(0, 2), 'orthogonal')[0])

    def test_min_2_connected_cells_touch_border_0_3(self):
        self.assertFalse(self.grid_dfs.are_min_2_connected_cells_touch_border(Position(0, 3), 'orthogonal')[0])

    def test_min_2_connected_cells_touch_border_1_1(self):
        self.assertTrue(self.grid_dfs.are_min_2_connected_cells_touch_border(Position(1, 1), 'orthogonal')[0])

    def test_min_2_diagonally_connected_cells_touch_border_0_0(self):
        self.assertTrue(self.grid_dfs_diagonal.are_min_2_connected_cells_touch_border(Position(0, 0), 'diagonal')[0])

    def test_min_2_diagonally_connected_cells_touch_border_0_1(self):
        self.assertTrue(self.grid_dfs_diagonal.are_min_2_connected_cells_touch_border(Position(0, 1), 'diagonal')[0])

    def test_min_2_diagonally_connected_cells_touch_border_1_3(self):
        self.assertTrue(self.grid_dfs_diagonal.are_min_2_connected_cells_touch_border(Position(1, 3), 'diagonal')[0])

    def test_min_2_diagonally_connected_cells_touch_border_2_3(self):
        self.assertFalse(self.grid_dfs_diagonal.are_min_2_connected_cells_touch_border(Position(2, 3), 'diagonal')[0])

    def test_min_2_diagonally_connected_cells_touch_border_3_4(self):
        self.assertFalse(self.grid_dfs_diagonal.are_min_2_connected_cells_touch_border(Position(3, 4), 'diagonal')[0])

    def test_find_min_2_connected_cells_touch_border_1(self):
        cells = self.grid_dfs.find_all_min_2_connected_cells_touch_border('1', 'orthogonal')
        expected_cells = {Position(0, 0), Position(0, 1)}
        self.assertEqual(1, len(cells))
        self.assertTrue(frozenset(expected_cells) in cells)

    def test_find_min_2_connected_cells_touch_border_2(self):
        cells = self.grid_dfs.find_all_min_2_connected_cells_touch_border('2', 'orthogonal')
        self.assertEqual(0, len(cells))

    def test_find_min_2_connected_cells_touch_border_3(self):
        cells = self.grid_dfs.find_all_min_2_connected_cells_touch_border('3', 'orthogonal')
        self.assertEqual(0, len(cells))

    def test_find_min_2_connected_cells_touch_border_8(self):
        cells = self.grid_dfs.find_all_min_2_connected_cells_touch_border('8', 'orthogonal')
        expected_cells = {Position(0, 4), Position(1, 0), Position(1, 1), Position(1, 3), Position(1, 4), Position(2, 0), Position(2, 4), Position(3, 0), Position(3, 1), Position(3, 2),
                          Position(3, 3), Position(3, 4)}
        self.assertEqual(1, len(cells))
        self.assertTrue(frozenset(expected_cells) in cells)

    def test_find_2_diagonally_connected_cells_touch_border_2(self):
        cells = self.grid_dfs_diagonal.find_all_min_2_connected_cells_touch_border('2', 'diagonal')
        expected_cells = {Position(0, 3), Position(1, 4)}
        self.assertEqual(1, len(cells))
        self.assertTrue(frozenset(expected_cells) in cells)

    def test_find_2_diagonally_connected_cells_touch_border_3(self):
        cells = self.grid_dfs_diagonal.find_all_min_2_connected_cells_touch_border('3', 'diagonal')
        self.assertEqual(0, len(cells))

    def test_find_2_diagonally_connected_cells_touch_border_5(self):
        cells = self.grid_dfs_diagonal.find_all_min_2_connected_cells_touch_border('5', 'diagonal')
        self.assertEqual(0, len(cells))

    def test_find_2_diagonally_connected_cells_touch_border_6(self):
        cells = self.grid_dfs_diagonal.find_all_min_2_connected_cells_touch_border('6', 'diagonal')
        self.assertEqual(0, len(cells))

    def test_find_2_diagonally_connected_cells_touch_border_7(self):
        cells = self.grid_dfs_diagonal.find_all_min_2_connected_cells_touch_border('7', 'diagonal')
        self.assertEqual(0, len(cells))

    def test_find_2_diagonally_connected_cells_touch_border_8(self):
        cells = self.grid_dfs_diagonal.find_all_min_2_connected_cells_touch_border('8', 'diagonal')
        expected_cells = {Position(0, 1), Position(1, 0)}
        self.assertEqual(1, len(cells))
        self.assertTrue(frozenset(expected_cells) in cells)

    def test_find_2_diagonally_connected_cells_touch_border_9(self):
        cells = self.grid_dfs_diagonal.find_all_min_2_connected_cells_touch_border('9', 'diagonal')
        expected_cells = {Position(1, 3), Position(2, 4), Position(3, 3)}
        self.assertEqual(1, len(cells))
        self.assertTrue(frozenset(expected_cells) in cells)

    def test_find_2_diagonally_connected_cells_touch_border_1(self):
        cells = self.grid_dfs_diagonal.find_all_min_2_connected_cells_touch_border('1', 'diagonal')
        expected_cells = {Position(0, 0), Position(0, 2), Position(1, 1), Position(2, 0), Position(2, 2)}
        self.assertEqual(1, len(cells))
        self.assertTrue(frozenset(expected_cells) in cells)

    def test_2_count_diagonally_connected_cells_touch_border_1(self):
        cells = self.grid_dfs_diagonal_border.find_all_min_2_connected_cells_touch_border('1', 'diagonal')
        expected_cells = {Position(0, 0), Position(1, 1), Position(2, 0)}
        expected_cells_2 = {Position(0, 4), Position(1, 3), Position(2, 4)}
        self.assertEqual(2, len(cells))
        self.assertTrue(frozenset(expected_cells) in cells)
        self.assertTrue(frozenset(expected_cells_2) in cells)

    def test_to_string_2x3(self):
        result_string = self.grid_2x3.to_console_string()
        result_string_cleaned = remove_ansi_escape_sequences(result_string)
        expected_string = "123\n456"
        self.assertEqual(expected_string, result_string_cleaned)

    def test_to_string_3x2(self):
        result_string = self.grid_3x2.to_console_string()
        result_string_cleaned = remove_ansi_escape_sequences(result_string)
        expected_string = "12\n34\n56"
        self.assertEqual(expected_string, result_string_cleaned)

    def test_to_string_bool(self):
        grid = Grid([
            [True, False, True],
            [False, True, False]
        ])
        expected_string = "101\n010"
        result_string = grid.to_console_string()
        result_string_cleaned = remove_ansi_escape_sequences(result_string)
        self.assertEqual(expected_string, result_string_cleaned)

    def test_to_color_string_3x3_with_color(self):
        color_grid = Grid([
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ])
        result_string = self.grid_3x3.to_console_string(color_grid)
        expected_string = f"{console_police_colors[0]}1{console_police_colors['end']}{console_police_colors[1]}2{console_police_colors['end']}{console_police_colors[2]}3{console_police_colors['end']}\n{console_police_colors[3]}4{console_police_colors['end']}{console_police_colors[4]}5{console_police_colors['end']}{console_police_colors[5]}6{console_police_colors['end']}\n{console_police_colors[6]}7{console_police_colors['end']}{console_police_colors[7]}8{console_police_colors['end']}{console_police_colors[8]}9{console_police_colors['end']}"
        self.assertEqual(expected_string, result_string)

    def test_to_color_string_3x3_with_background_color(self):
        background_color_grid = Grid([
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ])
        result_string = self.grid_3x3.to_console_string(None, background_color_grid)
        expected_string = f"{console_back_ground_colors[0]} 1 {console_back_ground_colors['end']}{console_back_ground_colors[1]} 2 {console_back_ground_colors['end']}{console_back_ground_colors[2]} 3 {console_back_ground_colors['end']}\n{console_back_ground_colors[3]} 4 {console_back_ground_colors['end']}{console_back_ground_colors[4]} 5 {console_back_ground_colors['end']}{console_back_ground_colors[5]} 6 {console_back_ground_colors['end']}\n{console_back_ground_colors[6]} 7 {console_back_ground_colors['end']}{console_back_ground_colors[7]} 8 {console_back_ground_colors['end']}{console_back_ground_colors[8]} 9 {console_back_ground_colors['end']}"
        self.assertEqual(expected_string, result_string)

    def test_get_adjacent_combinations_2on2(self):
        result_circular = self.grid_2x2.get_adjacent_combinations(2, 2, True)
        result_non_circular = self.grid_2x2.get_adjacent_combinations(2, 2, False)
        expected_result = [
            [True, True],
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_bit_array_adjacent_combinations_2on2(self):
        result_circular = self.grid_2x2.get_bit_array_adjacent_combinations(2, 2, True)
        result_non_circular = self.grid_2x2.get_bit_array_adjacent_combinations(2, 2, False)
        expected_result = [
            bitarray('11'),
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_adjacent_combinations_1on2(self):
        result_circular = self.grid_2x2.get_adjacent_combinations(2, 1, True)
        result_non_circular = self.grid_2x2.get_adjacent_combinations(2, 1, False)
        expected_result = [
            [True, False],
            [False, True],
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_bit_array_adjacent_combinations_1on2(self):
        result_circular = self.grid_2x2.get_bit_array_adjacent_combinations(2, 1, True)
        result_non_circular = self.grid_2x2.get_bit_array_adjacent_combinations(2, 1, False)
        expected_result = [
            bitarray('10'),
            bitarray('01'),
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_adjacent_combinations_3on3(self):
        result_circular = self.grid_2x2.get_adjacent_combinations(3, 3, True)
        result_non_circular = self.grid_2x2.get_adjacent_combinations(3, 3, False)
        expected_result = [
            [True, True, True],
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_bit_array_adjacent_combinations_3on3(self):
        result_circular = self.grid_2x2.get_bit_array_adjacent_combinations(3, 3, True)
        result_non_circular = self.grid_2x2.get_bit_array_adjacent_combinations(3, 3, False)
        expected_result = [
            bitarray('111'),
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_adjacent_combinations_1on3(self):
        result_circular = self.grid_2x2.get_adjacent_combinations(3, 1, True)
        result_non_circular = self.grid_2x2.get_adjacent_combinations(3, 1, False)
        expected_result = [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_bit_array_adjacent_combinations_1on3(self):
        result_circular = self.grid_2x2.get_bit_array_adjacent_combinations(3, 1, True)
        result_non_circular = self.grid_2x2.get_bit_array_adjacent_combinations(3, 1, False)
        expected_result = [
            bitarray('100'),
            bitarray('010'),
            bitarray('001'),
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_adjacent_combinations_2on3_circular(self):
        result_circular = self.grid_2x2.get_adjacent_combinations(3, 2, True)
        expected_result = [
            [True, True, False],
            [True, False, True],
            [False, True, True],
        ]
        self.assertEqual(expected_result, result_circular)

    def test_get_bit_array_adjacent_combinations_2on3_circular(self):
        result_circular = self.grid_2x2.get_bit_array_adjacent_combinations(3, 2, True)
        expected_result = [
            bitarray('110'),
            bitarray('011'),
            bitarray('101'),
        ]
        self.assertEqual(expected_result, result_circular)

    def test_get_adjacent_combinations_2on3_non_circular(self):
        result_non_circular = self.grid_2x2.get_adjacent_combinations(3, 2, False)
        expected_result = [
            [True, True, False],
            [False, True, True],
        ]
        self.assertEqual(expected_result, result_non_circular)

    def test_get_bit_array_adjacent_combinations_2on3_non_circular(self):
        result_non_circular = self.grid_2x2.get_bit_array_adjacent_combinations(3, 2, False)
        expected_result = [
            bitarray('110'),
            bitarray('011'),
        ]
        self.assertEqual(expected_result, result_non_circular)

    def test_get_adjacent_combinations_1on4(self):
        result_circular = self.grid_2x2.get_adjacent_combinations(4, 1, True)
        result_non_circular = self.grid_2x2.get_adjacent_combinations(4, 1, False)
        expected_result = [
            [True, False, False, False],
            [False, True, False, False],
            [False, False, True, False],
            [False, False, False, True],
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_bit_array_adjacent_combinations_1on4(self):
        result_circular = self.grid_2x2.get_bit_array_adjacent_combinations(4, 1, True)
        result_non_circular = self.grid_2x2.get_bit_array_adjacent_combinations(4, 1, False)
        expected_result = [
            bitarray('1000'),
            bitarray('0100'),
            bitarray('0010'),
            bitarray('0001'),
        ]
        self.assertEqual(expected_result, result_circular)
        self.assertEqual(expected_result, result_non_circular)

    def test_get_adjacent_combinations_2on4_circular(self):
        result_circular = self.grid_2x2.get_adjacent_combinations(4, 2, True)
        expected_result = [
            [True, True, False, False],
            [True, False, False, True],
            [False, True, True, False],
            [False, False, True, True],
        ]
        self.assertEqual(expected_result, result_circular)

    def test_get_bit_array_adjacent_combinations_2on4_circular(self):
        result_circular = self.grid_2x2.get_bit_array_adjacent_combinations(4, 2, True)
        expected_result = [
            bitarray('1100'),
            bitarray('0110'),
            bitarray('0011'),
            bitarray('1001'),
        ]
        self.assertEqual(expected_result, result_circular)

    def test_get_adjacent_combinations_2on4_non_circular(self):
        result_non_circular = self.grid_2x2.get_adjacent_combinations(4, 2, False)
        expected_result = [
            [True, True, False, False],
            [False, True, True, False],
            [False, False, True, True],
        ]
        self.assertEqual(expected_result, result_non_circular)

    def test_get_bit_array_adjacent_combinations_2on4_non_circular(self):
        result_non_circular = self.grid_2x2.get_bit_array_adjacent_combinations(4, 2, False)
        expected_result = [
            bitarray('1100'),
            bitarray('0110'),
            bitarray('0011'),
        ]
        self.assertEqual(expected_result, result_non_circular)

    def test_get_regions_2x2(self):
        regions = self.grid_2x2.get_regions()
        expected_regions = {
            '1': frozenset({Position(0, 0)}),
            '2': frozenset({Position(0, 1)}),
            '3': frozenset({Position(1, 0)}),
            '4': frozenset({Position(1, 1)}),
        }
        self.assertEqual(expected_regions, regions)

    def test_get_regions_grid_dfs(self):
        regions = self.grid_dfs.get_regions()
        expected_regions = {
            '1': frozenset({Position(0, 0), Position(0, 1)}),
            '2': frozenset({Position(0, 2), Position(1, 2)}),
            '3': frozenset({Position(0, 3), Position(2, 1)}),
            '5': frozenset({Position(2, 2), Position(2, 3)}),
            '8': frozenset(
                {Position(0, 4), Position(1, 0), Position(1, 1), Position(1, 3), Position(1, 4), Position(2, 0), Position(2, 4), Position(3, 0), Position(3, 1), Position(3, 2), Position(3, 3),
                 Position(3, 4)})
        }
        self.assertEqual(expected_regions, regions)

    def test_neighbors_positions_0_0(self):
        neighbors = self.grid_3x3.neighbors_positions(Position(0, 0))
        expected_neighbors = {Position(0, 1), Position(1, 0)}
        self.assertEqual(expected_neighbors, set(neighbors))

    def test_neighbors_positions_0_0_with_diagonal(self):
        neighbors = self.grid_3x3.neighbors_positions(Position(0, 0), 'diagonal')
        expected_neighbors = {Position(0, 1), Position(1, 0), Position(1, 1)}
        self.assertEqual(expected_neighbors, set(neighbors))

    def test_neighbors_positions_1_1(self):
        neighbors = self.grid_3x3.neighbors_positions(Position(1, 1))
        expected_neighbors = {Position(0, 1), Position(1, 0), Position(1, 2), Position(2, 1)}
        self.assertEqual(expected_neighbors, set(neighbors))

    def test_neighbors_positions_1_1_with_diagonal(self):
        neighbors = self.grid_3x3.neighbors_positions(Position(1, 1), 'diagonal')
        expected_neighbors = {Position(0, 1), Position(1, 0), Position(1, 2), Position(2, 1), Position(0, 0), Position(0, 2), Position(2, 0), Position(2, 2)}
        self.assertEqual(expected_neighbors, set(neighbors))

    def test_neighbors_positions_3_3_with_walls(self):
        grid = Grid([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        grid.add_walls(
            {
                frozenset([Position(0, 1), Position(1, 1)]),
                frozenset([Position(1, 0), Position(1, 1)]),
                frozenset([Position(2, 1), Position(1, 1)]),
                frozenset([Position(1, 2), Position(1, 1)]),
            }
        )
        neighbors_1_1 = grid.neighbors_positions(Position(1, 1))
        self.assertEqual(0, len(neighbors_1_1))

        neighbors_0_1 = grid.neighbors_positions(Position(0, 1))
        expected_neighbors_0_1 = {Position(0, 0), Position(0, 2)}
        self.assertEqual(expected_neighbors_0_1, neighbors_0_1)

        neighbors_1_0 = grid.neighbors_positions(Position(1, 0))
        expected_neighbors_1_0 = {Position(0, 0), Position(2, 0)}
        self.assertEqual(expected_neighbors_1_0, neighbors_1_0)

        neighbors_1_2 = grid.neighbors_positions(Position(1, 2))
        expected_neighbors_1_2 = {Position(0, 2), Position(2, 2)}
        self.assertEqual(expected_neighbors_1_2, neighbors_1_2)

        neighbors_2_1 = grid.neighbors_positions(Position(2, 1))
        expected_neighbors_2_1 = {Position(2, 0), Position(2, 2)}
        self.assertEqual(expected_neighbors_2_1, neighbors_2_1)

    def test_repr_non_empty_grid(self):
        grid = Grid([[1, 2], [3, 4]])
        expected_repr = "1 2\n3 4"
        self.assertEqual(repr(grid), expected_repr)

    def test_repr_empty_grid(self):
        grid = Grid([[]])
        expected_repr = "Grid.empty()"
        self.assertEqual(repr(grid), expected_repr)

    def test_repr_fully_populated_grid(self):
        grid = Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        expected_repr = "1 2 3\n4 5 6\n7 8 9"
        self.assertEqual(repr(grid), expected_repr)

    def test_repr_with_complex_data_types(self):
        complex_grid = Grid([
            [{'a': 1}, {'b': 2}],
            [[1, 2], [3, 4]],
            [(1, 2), (3, 4)]
        ])
        expected_repr = "{'a': 1} {'b': 2}\n[1, 2] [3, 4]\n(1, 2) (3, 4)"
        self.assertEqual(repr(complex_grid), expected_repr)

    def test_find_all_positions_in(self):
        grid = Grid([
            [1, 1],
            [1, None],
            [1, None]
        ])
        grid1 = Grid([
            [1, 1, 1, 4, 1, 1],
            [1, 1, 1, 5, 1, 8],
            [1, 1, 1, 1, 1, 2],
            [6, 1, 7, 2, 2, 2],
        ])
        expected_positions = {Position(0, 0), Position(0, 1), Position(0, 4), Position(1, 1)}
        positions = grid.find_all_positions_in(grid1)
        self.assertEqual(expected_positions, positions)


if __name__ == '__main__':
    unittest.main()
