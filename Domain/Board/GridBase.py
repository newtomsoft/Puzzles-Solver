from collections import defaultdict
from itertools import combinations
from typing import FrozenSet, Generator, TypeVar, Iterable, Any

import numpy as np
from bitarray import bitarray

from Domain.Board.Direction import Direction
from Domain.Board.Position import Position
from Domain.Puzzles.Pipes.PipeShapeTransition import PipeShapeTransition
from Utils.colors import console_back_ground_colors, console_police_colors

T = TypeVar('T')


def safe_max(row):
    return max(x for x in row if x is not None)


class GridBase[T]:
    def __init__(self, matrix: list[list[T]]):
        self._matrix = matrix
        self.rows_number = len(matrix)
        self.columns_number = len(matrix[0])
        self._walls: set[FrozenSet[Position]] = set()

    def __getitem__(self, key) -> T:
        if isinstance(key, Position):
            return self._matrix[key.r][key.c]
        if isinstance(key, tuple):
            return self._matrix[key[0]][key[1]]
        return self._matrix[key]

    def __setitem__(self, key, value):
        if isinstance(key, Position):
            self._matrix[key.r][key.c] = value
        elif isinstance(key, tuple):
            self._matrix[key[0]][key[1]] = value
        else:
            self._matrix[key] = value

    def __eq__(self, other):
        if not issubclass(type(other), GridBase):
            return False
        if all(isinstance(cell, bool) for cell in self._matrix):
            return all(value == other.value(position) for position, value in self)
        return self.matrix == other.matrix

    def __contains__(self, item: Position | T) -> bool:
        if item is None:
            return False
        return 0 <= item.r < self.rows_number and 0 <= item.c < self.columns_number

    def __iter__(self) -> Generator[tuple[Position, T | Any], None, None]:
        for r, row in enumerate(self._matrix):
            for c, cell in enumerate(row):
                yield Position(r, c), cell

    def __repr__(self) -> str:
        if self.is_empty():
            return 'Grid.empty()'
        if isinstance(self[Position(0, 0)], PipeShapeTransition):
            return '\n'.join(''.join(str(cell) for cell in row) for row in self._matrix)
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self._matrix)

    def __hash__(self):
        return hash(str(self._matrix))

    def min_value(self) -> float:
        matrice_np = np.array(self._matrix, dtype=float)
        return float(np.nanmin(matrice_np))

    def max_value(self) -> float:
        matrice_np = np.array(self._matrix, dtype=float)
        return float(np.nanmax(matrice_np))

    @property
    def matrix(self):
        return self._matrix

    @property
    def walls(self):
        return self._walls

    @staticmethod
    def empty() -> 'GridBase':
        return GridBase([[]])

    def value(self, r_or_position, c=None) -> T:
        if isinstance(r_or_position, Position):
            return self._matrix[r_or_position.r][r_or_position.c]
        return self._matrix[r_or_position][c]

    def set_value(self, position: Position, value):
        self._matrix[position.r][position.c] = value

    def get_index_from_position(self, position: Position) -> int:
        return position.r * self.columns_number + position.c

    def get_positions(self):
        return [Position(r, c) for r in range(self.rows_number) for c in range(self.columns_number)]

    def get_position_from_index(self, index: int) -> Position:
        return Position(index // self.columns_number, index % self.columns_number)

    def to_console_string(self, police_color_grid=None, back_ground_color_grid=None, interline=False):
        matrix = self._matrix.copy()
        if all([isinstance(self._matrix[r][c], bool) for r in range(self.rows_number) for c in range(self.columns_number)]):
            matrix = [[1 if self._matrix[r][c] else 0 for c in range(self.columns_number)] for r in range(self.rows_number)]
        color_matrix = [[console_police_colors[police_color_grid.value(r, c) % (len(console_police_colors) - 1)] if police_color_grid else '' for c in range(self.columns_number)]
                        for r in
                        range(self.rows_number)]
        background_color_matrix = [
            [console_back_ground_colors[back_ground_color_grid.value(r, c) % (len(console_police_colors) - 1)] if back_ground_color_grid else '' for c in
             range(self.columns_number)] for r in
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

    def get_regions(self) -> dict[int, FrozenSet[Position]]:
        regions = defaultdict(set)
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._matrix[r][c] not in regions:
                    regions[self._matrix[r][c]] = set()
                regions[self._matrix[r][c]].add(Position(r, c))
        return {key: frozenset(value) for key, value in regions.items()} if regions else {}

    def are_cells_connected(self, value: T = True, mode='orthogonal') -> bool:
        position = self._get_cell_of_value(value)
        if position is None:
            return False
        visited = self._depth_first_search(position, value, mode)
        return len(visited) == sum(cell == value for row in self._matrix for cell in row)

    def are_all_cells_connected(self, mode='orthogonal') -> bool:
        return all([self.are_cells_connected(region_key, mode) for region_key in self.get_regions().keys()])

    def get_all_shapes(self, value=True, mode='orthogonal') -> set[FrozenSet[Position]]:
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

    def are_min_2_connected_cells_touch_border(self, position, mode='orthogonal') -> tuple[bool, set[Position]]:
        value = self.value(position)
        visited = self._depth_first_search(position, value, mode)
        if len(visited) <= 1:
            return False, set()
        border_cells = set()
        for cell in visited:
            if cell[0] == 0 or cell[0] == self.rows_number - 1 or cell[1] == 0 or cell[1] == self.columns_number - 1:
                border_cells.add(cell)
        return len(border_cells) >= 2, visited

    def find_all_min_2_connected_cells_touch_border(self, value, mode='orthogonal') -> set[FrozenSet[Position]]:
        excluded = []
        cells_sets: set[FrozenSet[Position]] = set()
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

    def _depth_first_search(self, position: Position, value, mode='orthogonal', visited=None) -> set[Position]:
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

    def _get_cell_of_value(self, value, excluded=None) -> Position | None:
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

    def set_walls(self, walls: set[FrozenSet[Position]]):
        self._walls = walls

    def add_wall(self, wall: list[Position]):
        if len(wall) != 2:
            raise ValueError("Un mur doit contenir exactement deux positions")
        self._walls.add(frozenset(wall))

    def copy_walls_from_grid(self, other_grid: 'GridBase'):
        self._walls = other_grid._walls

    @staticmethod
    def list_to_string(values):
        return sum(values)

    def is_empty(self):
        return self == GridBase.empty()

    def all_orthogonal_positions(self, position: Position) -> set[Position]:
        return set(self.all_positions_up(position)) | set(self.all_positions_down(position)) | set(self.all_positions_left(position)) | set(self.all_positions_right(position))

    def neighbors_positions(self, position: Position, mode='orthogonal') -> set[Position]:
        """mode : orthogonal, diagonal, diagonal_only"""
        if mode == 'diagonal_only':
            return {self.neighbor_up_left(position), self.neighbor_up_right(position), self.neighbor_down_left(position), self.neighbor_down_right(position)} - {None}

        orthogonal_neighbors = {self.neighbor_up(position), self.neighbor_down(position), self.neighbor_left(position), self.neighbor_right(position)} - {None}
        if mode == 'orthogonal':
            return orthogonal_neighbors

        if mode == 'diagonal' or mode == 'all':
            diagonal_neighbors = {self.neighbor_up_left(position), self.neighbor_up_right(position), self.neighbor_down_left(position), self.neighbor_down_right(position)} - {None}
            return orthogonal_neighbors | diagonal_neighbors

        raise ValueError(f"Invalid mode: {mode}")

    def neighbor_up(self, position: Position) -> Position:
        return position.up if position.up in self and {position, position.up} not in self._walls else None

    def neighbor_down(self, position: Position) -> Position:
        return position.down if position.down in self and {position, position.down} not in self._walls else None

    def neighbor_left(self, position: Position) -> Position:
        return position.left if position.left in self and {position, position.left} not in self._walls else None

    def neighbor_right(self, position: Position) -> Position:
        return position.right if position.right in self and {position, position.right} not in self._walls else None

    def neighbor_up_left(self, position: Position) -> Position:
        return position.up_left if position.up_left in self else None  # check if wall is not between position and position.up_left ?

    def neighbor_up_right(self, position: Position) -> Position:
        return position.up_right if position.up_right in self else None  # check if wall is not between position and position.up_right ?

    def neighbor_down_left(self, position: Position) -> Position:
        return position.down_left if position.down_left in self else None  # check if wall is not between position and position.down_left ?

    def neighbor_down_right(self, position: Position) -> Position:
        return position.down_right if position.down_right in self else None  # check if wall is not between position and position.down_right ?

    def neighbors_values(self, position: Position, mode='orthogonal') -> list[T]:
        """mode : orthogonal, diagonal, diagonal_only"""
        return [self.value(neighbor) for neighbor in self.neighbors_positions(position, mode)]

    def all_positions_in_direction(self, position: Position, direction: Direction) -> list[Position]:
        if direction == Direction.up():
            return self.all_positions_up(position)
        if direction == Direction.down():
            return self.all_positions_down(position)
        if direction == Direction.left():
            return self.all_positions_left(position)
        if direction == Direction.right():
            return self.all_positions_right(position)
        raise ValueError(f"Invalid direction: {direction}")

    def all_positions_up(self, position: Position) -> list[Position]:
        positions = []
        while position.up in self and {position, position.up} not in self._walls:
            position = position.up
            positions.append(position)
        return positions

    def all_positions_down(self, position: Position) -> list[Position]:
        positions = []
        while position.down in self and {position, position.down} not in self._walls:
            position = position.down
            positions.append(position)
        return positions

    def all_positions_left(self, position: Position) -> list[Position]:
        positions = []
        while position.left in self and {position, position.left} not in self._walls:
            position = position.left
            positions.append(position)
        return positions

    def all_positions_right(self, position: Position) -> list[Position]:
        positions = []
        while position.right in self and {position, position.right} not in self._walls:
            position = position.right
            positions.append(position)
        return positions

    def all_positions_up_right(self, position: Position) -> list[Position]:
        positions = []
        while position.up_right in self and {position, position.up_right} not in self._walls:
            position = position.up_right
            positions.append(position)
        return positions

    def all_positions_up_left(self, position: Position) -> list[Position]:
        positions = []
        while position.up_left in self and {position, position.up_left} not in self._walls:
            position = position.up_left
            positions.append(position)
        return positions

    def all_positions_down_right(self, position: Position) -> list[Position]:
        positions = []
        while position.down_right in self and {position, position.down_right} not in self._walls:
            position = position.down_right
            positions.append(position)
        return positions

    def all_positions_down_left(self, position: Position) -> list[Position]:
        positions = []
        while position.down_left in self and {position, position.down_left} not in self._walls:
            position = position.down_left
            positions.append(position)
        return positions

    def straddled_neighbors_positions(self, position: Position) -> set[Position]:
        return {neighbor for neighbor in position.straddled_neighbors() if neighbor in self}

    def find_all_positions_in(self, grid: 'GridBase', value_to_ignore=None) -> set[Position]:
        positions = set()
        for r in range(grid.rows_number - self.rows_number + 1):
            for c in range(grid.columns_number - self.columns_number + 1):
                position = Position(r, c)
                if self._is_in_grid_at_position(grid, position, value_to_ignore):
                    positions.add(position)
        return positions

    def _is_in_grid_at_position(self, grid: 'GridBase', position: Position, value_to_ignore):
        for current_position, value in [(self_position + position, value) for self_position, value in self if value is not value_to_ignore]:
            if current_position.r >= grid.rows_number or current_position.c >= grid.columns_number:
                return False
            if value != grid[current_position]:
                return False
        return True

    @classmethod
    def from_positions(cls, positions: Iterable[Position], set_value=True, unset_value=False) -> tuple['GridBase', Position]:
        min_r = min(position.r for position in positions)
        max_r = max(position.r for position in positions)
        min_c = min(position.c for position in positions)
        max_c = max(position.c for position in positions)
        matrix = [[unset_value for _ in range(max_c - min_c + 1)] for _ in range(max_r - min_r + 1)]
        for position in [position - Position(min_r, min_c) for position in positions]:
            matrix[position.r][position.c] = set_value
        return cls(matrix), Position(min_r, min_c)

    def find_different_neighbors_positions(self) -> list[tuple[Position, Position]]:
        pairs: list[tuple[Position, Position]] = list()
        min_value = self.min_value()
        max_value = self.max_value()

        for cell_value in range(min_value, max_value + 1):
            for cell_position in [position for position, value in self if value == cell_value]:
                for neighbor_position in self.neighbors_positions(cell_position):
                    neighbor_value = self[neighbor_position]
                    if neighbor_value != cell_value:
                        pair = (cell_position, neighbor_position) if cell_position < neighbor_position else (neighbor_position, cell_position)
                        if pair not in pairs:
                            pairs.append(pair)
        return pairs
