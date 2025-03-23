from typing import Tuple

from Domain.Grid.WrappedGrid import WrappedGrid
from Domain.Position import Position
from Pipes.Pipe import Pipe


class WrappedPipesGrid(WrappedGrid[Pipe]):
    def __init__(self, input_matrix: list[list[Pipe]]):
        super().__init__(input_matrix)

    def get_connected_positions_and_is_loop(self) -> Tuple[list[set[Position]], bool]:
        total_positions = self.columns_number * self.rows_number
        visited_list: list[set[Position]] = []
        visited_flat: set[Position] = set()
        is_loop = False
        while len(visited_flat) != total_positions:
            position = next(position for position, _ in self if position not in visited_flat)
            visited_in_this_pass, is_loop_in_this_pass = self._depth_first_search_pipes_and_is_loop(position)
            if is_loop_in_this_pass:
                is_loop = True
            visited_list.append(visited_in_this_pass)
            visited_flat.update(visited_in_this_pass)
        return visited_list, is_loop

    def _depth_first_search_pipes_and_is_loop(self, position: Position, visited_positions=None, forbidden_direction=None) -> Tuple[set[Position], bool]:
        if visited_positions is None:
            visited_positions = set()
        if position in visited_positions:
            return visited_positions, True
        visited_positions.add(position)

        current_pipe = self[position]
        connected_to = current_pipe.get_connected_to()
        for direction in [direction for direction in connected_to if direction != forbidden_direction]:
            next_pos = position.after(direction)
            if {position, next_pos} in self._walls:
                continue
            next_pos = self.normalize_position(next_pos)
            next_pipe = self[next_pos]
            if direction.opposite in next_pipe.get_connected_to():
                self._depth_first_search_pipes_and_is_loop(next_pos, visited_positions, direction.opposite)

        return visited_positions, False

    def normalize_position(self, position: Position) -> Position:
        if position.r < 0:
            position = Position(self.rows_number - 1, position.c)
        if position.r >= self.rows_number:
            position = Position(0, position.c)
        if position.c < 0:
            position = Position(position.r, self.columns_number - 1)
        if position.c >= self.columns_number:
            position = Position(position.r, 0)
        return position
