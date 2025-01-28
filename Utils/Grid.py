from collections import defaultdict
from itertools import combinations
from typing import Tuple, FrozenSet, Dict, List, TypeVar, Set, Generator

from bitarray import bitarray

from Utils.Position import Position
from Utils.colors import console_back_ground_colors, console_police_colors

T = TypeVar('T')


class Grid[T]:
    def __init__(self, matrix: List[List[T]]):
        self._matrix = matrix
        self.rows_number = len(matrix)
        self.columns_number = len(matrix[0])

    def __getitem__(self, item: T) -> T:
        if isinstance(item, Position):
            return self._matrix[item.r][item.c]
        if isinstance(item, tuple):
            return self._matrix[item[0]][item[1]]
        return self._matrix[item]

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        if all(isinstance(cell, bool) for cell in self._matrix):
            return all(value == other.value(position) for position, value in self)
        return self.matrix == other.matrix

    def __contains__(self, item):
        if isinstance(item, Position):
            return 0 <= item.r < self.rows_number and 0 <= item.c < self.columns_number
        raise TypeError(f'Position expected, got {type(item)}')

    def __iter__(self) -> Generator[Tuple[Position, T]]:
        for r, row in enumerate(self._matrix):
            for c, cell in enumerate(row):
                yield Position(r, c), cell

    def __str__(self) -> str:
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self._matrix)

    def __repr__(self) -> str:
        if self.is_empty():
            return 'Grid.empty()'
        return self.__str__()

    @property
    def matrix(self):
        return self._matrix

    @staticmethod
    def empty() -> 'Grid':
        return Grid([[]])

    def value(self, r_or_position, c=None) -> T:
        if isinstance(r_or_position, Position):
            return self._matrix[r_or_position.r][r_or_position.c]
        return self._matrix[r_or_position][c]

    def set_value(self, position: Position, value):
        self._matrix[position.r][position.c] = value

    def get_index(self, position: Position) -> int:
        return position.r * self.columns_number + position.c

    def to_console_string(self, police_color_grid=None, back_ground_color_grid=None, interline=False):
        matrix = self._matrix.copy()
        if all([isinstance(self._matrix[r][c], bool) for r in range(self.rows_number) for c in range(self.columns_number)]):
            matrix = [[1 if self._matrix[r][c] else 0 for c in range(self.columns_number)] for r in range(self.rows_number)]
        color_matrix = [[console_police_colors[police_color_grid.value(r, c) % (len(console_police_colors) - 1)] if police_color_grid else '' for c in range(self.columns_number)] for r in
                        range(self.rows_number)]
        background_color_matrix = [
            [console_back_ground_colors[back_ground_color_grid.value(r, c) % (len(console_police_colors) - 1)] if back_ground_color_grid else '' for c in range(self.columns_number)] for r in
            range(self.rows_number)]
        end_color = console_back_ground_colors['end'] if police_color_grid or back_ground_color_grid else ''
        end_space = ' ' if back_ground_color_grid else ''
        result = []
        cell_len = max(len(f'{cell}') for row in matrix for cell in row)
        for r in range(self.rows_number):
            result.append(self._row_to_string(matrix, r, cell_len, background_color_matrix, color_matrix, end_color, end_space))
            if interline and r < self.rows_number - 1:
                result.append(''.join(f'{background_color_matrix[r][c]}{end_color}' for c in range(self.columns_number)))
        return '\n'.join(result)

    def _row_to_string(self, matrix, r, max_len, background_color_matrix, color_matrix, end_color, end_space):
        return ''.join(f'{background_color_matrix[r][c]}{color_matrix[r][c]}{end_space}{matrix[r][c]}{end_space}{end_color}'.rjust(max_len) for c in range(self.columns_number))

    def get_regions(self) -> Dict[int, FrozenSet[Position]]:
        regions = defaultdict(set)
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._matrix[r][c] not in regions:
                    regions[self._matrix[r][c]] = set()
                regions[self._matrix[r][c]].add(Position(r, c))
        return {key: frozenset(value) for key, value in regions.items()} if regions else {}

    def are_all_cells_connected(self, value=True, mode='orthogonal') -> bool:
        position = self._get_cell_of_value(value)
        if position is None:
            return False
        visited = self._depth_first_search(position, value, mode)
        return len(visited) == sum(cell == value for row in self._matrix for cell in row)

    def get_all_shapes(self, value=True, mode='orthogonal') -> Set[FrozenSet[Position]]:
        excluded = []
        shapes = set()
        while True:
            position = self._get_cell_of_value(value, excluded)
            if position is None:
                break
            if any(position in shape for shape in shapes):
                excluded.append(position)
                continue
            visited = self._depth_first_search(position, value, mode)
            shapes.add(frozenset(visited))
            excluded.append(position)
        return shapes

    def are_min_2_connected_cells_touch_border(self, position, mode='orthogonal') -> Tuple[bool, set[Position]]:
        value = self.value(position)
        visited = self._depth_first_search(position, value, mode)
        if len(visited) <= 1:
            return False, set()
        border_cells = set()
        for cell in visited:
            if cell[0] == 0 or cell[0] == self.rows_number - 1 or cell[1] == 0 or cell[1] == self.columns_number - 1:
                border_cells.add(cell)
        return len(border_cells) >= 2, visited

    def find_all_min_2_connected_cells_touch_border(self, value, mode='orthogonal') -> Set[FrozenSet[Position]]:
        excluded = []
        cells_sets: Set[FrozenSet[Position]] = set()
        while True:
            position = self._get_cell_of_value(value, excluded)
            if position is None:
                break
            if any(position in cells_set for cells_set in cells_sets):
                excluded.append(position)
                continue
            are_touch_border, cells = self.are_min_2_connected_cells_touch_border(position, mode)
            if are_touch_border:
                cells_sets.add(frozenset(cells))
            excluded.append(position)
        return cells_sets

    def _depth_first_search(self, position: Position, value, mode='orthogonal', visited=None) -> Set[Position]:
        if visited is None:
            visited = set()
        if (self.value(position) != value) or (position in visited):
            return visited
        visited.add(position)

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] if mode != 'diagonal' else [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            if 0 <= position.r + dr < self.rows_number and 0 <= position.c + dc < self.columns_number and (position.r + dr, position.c + dc) not in visited:
                current_position = position + Position(dr, dc)
                if self.value(current_position) == value:
                    new_visited = self._depth_first_search(current_position, value, mode, visited)
                    if new_visited != visited:
                        return new_visited

        return visited

    def _get_cell_of_value(self, value, excluded=None) -> Position or None:
        if excluded is None:
            excluded = []
        return next((Position(i, j) for i in range(self.rows_number) for j in range(self.columns_number) if self._matrix[i][j] == value and Position(i, j) not in excluded), None)

    @staticmethod
    def get_adjacent_combinations(neighbour_length, block_length, circular) -> list[list[bool]]:
        if block_length == 0:
            return [[False for _ in range(neighbour_length)]]
        if block_length == neighbour_length:
            return [[True for _ in range(neighbour_length)]]
        result = []
        for combo in combinations(range(neighbour_length), block_length):
            cell_adjacent = [True for i in range(1, block_length) if combo[i] - combo[i - 1] == 1]
            if circular and combo[0] + neighbour_length - combo[-1] == 1:
                cell_adjacent.append(True)
            if cell_adjacent.count(True) == block_length - 1:
                indexes = [index in combo for index in range(neighbour_length)]
                result.append(indexes)
        return result

    @staticmethod
    def get_bit_array_adjacent_combinations(neighbour_length, block_length, circular) -> list[bitarray]:
        bitarrays = []
        first_bitarray = bitarray(neighbour_length)
        for i in range(block_length):
            first_bitarray[i] = True
        bitarrays.append(first_bitarray)
        current_bitarray = first_bitarray
        for i in range(neighbour_length - block_length):
            current_bitarray = current_bitarray >> 1
            if current_bitarray not in bitarrays:
                bitarrays.append(current_bitarray)
        if circular:
            for i in range(block_length - 1):
                current_bitarray = current_bitarray >> 1
                current_bitarray[0] = True
                if current_bitarray not in bitarrays:
                    bitarrays.append(current_bitarray)
        return bitarrays

    @staticmethod
    def list_to_string(values):
        return sum(values)

    def is_empty(self):
        return self == Grid.empty()

    def neighbors_positions(self, position: Position, mode='orthogonal') -> list[Position]:
        return [position for position in position.neighbors(mode) if position in self]

    def neighbors_values(self, position: Position, mode='orthogonal') -> list[T]:
        return [self.value(neighbor) for neighbor in self.neighbors_positions(position, mode)]

    def straddled_neighbors_positions(self, position: Position) -> Set[Position]:
        return {neighbor for neighbor in position.straddled_neighbors() if neighbor in self}
