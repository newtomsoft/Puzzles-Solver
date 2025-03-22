from collections import defaultdict
from itertools import combinations
from typing import Tuple, FrozenSet, Dict, List, TypeVar, Set, Generic, Iterable

from bitarray import bitarray

from Utils.Grid import Grid
from Utils.GridBase import GridBase
from Utils.Position import Position

T = TypeVar('T')


class WrappedGrid(GridBase[T], Generic[T]):
    def __init__(self, matrix: List[List[T]]):
        super().__init__(matrix)

    def __getitem__(self, key) -> T:
        if isinstance(key, Position):
            key = Position(key.r % self.rows_number, key.c % self.columns_number)
            try:
                return self._matrix[key.r][key.c]
            except IndexError:
                return None

        if isinstance(key, tuple):
            return self._matrix[key[0]][key[1]]
        return self._matrix[key]

    def __contains__(self, item):
        if not isinstance(item, Position):
            raise TypeError(f'Position expected, got {type(item)}')
        return True

    def get_regions(self) -> Dict[int, FrozenSet[Position]]:
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

    def neighbor_up(self, position: Position) -> Position:
        return position.up if position.up in self else None

    def neighbor_down(self, position: Position) -> Position:
        return position.down if position.down in self else None

    def neighbor_left(self, position: Position) -> Position:
        return position.left if position.left in self else None

    def neighbor_right(self, position: Position) -> Position:
        return position.right if position.right in self else None

    def neighbors_values(self, position: Position, mode='orthogonal') -> list[T]:
        return [self.value(neighbor) for neighbor in self.neighbors_positions(position, mode)]

    def straddled_neighbors_positions(self, position: Position) -> Set[Position]:
        return {neighbor for neighbor in position.straddled_neighbors() if neighbor in self}

    def find_all_positions_in(self, grid: 'Grid', value_to_ignore=None) -> Set[Position]:
        positions = set()
        for r in range(grid.rows_number - self.rows_number + 1):
            for c in range(grid.columns_number - self.columns_number + 1):
                position = Position(r, c)
                if self._is_in_grid_at_position(grid, position, value_to_ignore):
                    positions.add(position)
        return positions

    def _is_in_grid_at_position(self, grid: 'Grid', position: Position, value_to_ignore):
        for current_position, value in [(self_position + position, value) for self_position, value in self if value is not value_to_ignore]:
            if current_position.r >= grid.rows_number or current_position.c >= grid.columns_number:
                return False
            if value != grid[current_position]:
                return False
        return True

    @classmethod
    def from_positions(cls, positions: Iterable[Position], set_value=True, unset_value=False) -> ('Grid', Position):
        min_r = min(position.r for position in positions)
        max_r = max(position.r for position in positions)
        min_c = min(position.c for position in positions)
        max_c = max(position.c for position in positions)
        matrix = [[unset_value for _ in range(max_c - min_c + 1)] for _ in range(max_r - min_r + 1)]
        for position in [position - Position(min_r, min_c) for position in positions]:
            matrix[position.r][position.c] = set_value
        return cls(matrix), Position(min_r, min_c)
