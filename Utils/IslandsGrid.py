from typing import Dict

from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.Island import Island
from Utils.Position import Position


class IslandGrid(Grid[Island]):
    def __init__(self, grid: Grid):
        self.islands: Dict[Position, Island] = {}
        for position, bridges in grid:
            if bridges != 0:
                self.islands[position] = Island(position, bridges)

        if len(self.islands) == 0:
            super().__init__([[]])
            self.islands = {}
            return

        matrix = [[self.islands[position] if (position := Position(r, c)) in self.islands.keys() else 0 for c in range(grid.columns_number)] for r in range(grid.rows_number)]
        super().__init__(matrix)
        self._compute_possible_bridges()
        self.possible_crossover_bridge = self._compute_possible_crossover_bridges()

    @staticmethod
    def empty() -> 'IslandGrid':
        return IslandGrid(Grid.empty())

    def _compute_possible_bridges(self):
        for island in self.islands.values():
            min_distances = {}
            for other_island in self.islands.values():
                direction = island.position.direction_to(other_island.position)
                if direction != Direction.right() and direction != Direction.left() and direction != Direction.up() and direction != Direction.down():
                    continue
                distance = island.position.distance_to(other_island.position)
                if direction == Direction.right() and distance < min_distances.get(Direction.right(), (float('inf'), None))[0]:
                    min_distances[Direction.right()] = (distance, other_island.position)
                    continue
                if direction == Direction.left() and distance < min_distances.get(Direction.left(), (float('inf'), None))[0]:
                    min_distances[Direction.left()] = (distance, other_island.position)
                    continue
                if direction == Direction.up() and distance < min_distances.get(Direction.up(), (float('inf'), None))[0]:
                    min_distances[Direction.up()] = (distance, other_island.position)
                    continue
                if direction == Direction.down() and distance < min_distances.get(Direction.down(), (float('inf'), None))[0]:
                    min_distances[Direction.down()] = (distance, other_island.position)
                    continue

            if min_distances.get(Direction.right()) is not None:
                island.direction_position_bridges[Direction.right()] = min_distances[Direction.right()][1], 0
            if min_distances.get(Direction.left()) is not None:
                island.direction_position_bridges[Direction.left()] = min_distances[Direction.left()][1], 0
            if min_distances.get(Direction.up()) is not None:
                island.direction_position_bridges[Direction.up()] = min_distances[Direction.up()][1], 0
            if min_distances.get(Direction.down()) is not None:
                island.direction_position_bridges[Direction.down()] = min_distances[Direction.down()][1], 0

    def _compute_possible_crossover_bridges(self) -> list[Dict[Position, Direction]]:
        possible_multiples_crossover_positions: Dict[Position, Dict[Position, Direction]] = {}
        for island in self.islands.values():
            island_position = island.position
            for direction, (other_position, _) in island.direction_position_bridges.items():
                if island_position.distance_to(other_position) == 1 or direction == Direction.left() or direction == Direction.up():
                    continue
                cross_positions = island_position.get_positions_to(other_position)
                for cross_position in cross_positions:
                    if possible_multiples_crossover_positions.get(cross_position) is None:
                        possible_multiples_crossover_positions[cross_position] = {}
                    possible_multiples_crossover_positions[cross_position][island_position] = direction

        possible_crossover_bridges = [
            directions_and_positions
            for directions_and_positions in possible_multiples_crossover_positions.values()
            if len(directions_and_positions) == 2
        ]
        return possible_crossover_bridges

    def __repr__(self) -> str:
        if self.is_empty():
            return 'Grid.empty()'
        return self.__str__()

    def get_connected_positions(self, exclude_without_bridge=False) -> list[set[Position]]:
        concerned_islands_count = len(self.islands) if not exclude_without_bridge else sum(1 for island in self.islands.values() if island.bridges_count != 0)
        visited_list: list[set[Position]] = []
        visited_flat: set[Position] = set()
        while len(visited_flat) != concerned_islands_count:
            position = next(island.position for island in self.islands.values() if island.position not in visited_flat) if not exclude_without_bridge else next((island.position for island in self.islands.values() if island.bridges_count != 0 and island.position not in visited_flat), None)
            visited = self._depth_first_search_islands(position)
            visited_list.append(visited)
            visited_flat.update(visited)
        return visited_list

    def _depth_first_search_islands(self, position: Position, visited_positions=None) -> set[Position]:
        if visited_positions is None:
            visited_positions = set()
        if position in visited_positions:
            return visited_positions
        visited_positions.add(position)
        position_bridges = self.islands[position].direction_position_bridges.values()
        for position_bridge in position_bridges:
            if position_bridge[1] == 0:
                continue
            current_position = position_bridge[0]
            if current_position not in visited_positions:
                new_visited_positions = self._depth_first_search_islands(current_position, visited_positions)
                if new_visited_positions != visited_positions:
                    return new_visited_positions

        return visited_positions

    def __str__(self) -> str:
        matrix = self._matrix.copy()
        result = []
        for r in range(self.rows_number):
            result.append(''.join(f'{self.string(matrix[r][c])}' for c in range(self.columns_number)))
        return '\n'.join(result)

    def _row_to_string(self, matrix, r, max_len, background_color_matrix, color_matrix, end_color, end_space):
        return ''.join(f'{self.string(matrix[r][c])}' for c in range(self.columns_number))

    @staticmethod
    def string(island: Island) -> str:
        if isinstance(island, int):
            return ' · '
        if island.has_no_bridge():
            return '   '
        if Direction.up() in island.direction_position_bridges and Direction.right() in island.direction_position_bridges:
            return ' └─'
        if Direction.up() in island.direction_position_bridges and Direction.left() in island.direction_position_bridges:
            return '─┘ '
        if Direction.down() in island.direction_position_bridges and Direction.right() in island.direction_position_bridges:
            return ' ┌─'
        if Direction.down() in island.direction_position_bridges and Direction.left() in island.direction_position_bridges:
            return '─┐ '
        if Direction.up() in island.direction_position_bridges and Direction.down() in island.direction_position_bridges:
            return ' │ '
        if Direction.right() in island.direction_position_bridges and Direction.left() in island.direction_position_bridges:
            return '───'
        if Direction.up() in island.direction_position_bridges:
            return ' │ '
        if Direction.down() in island.direction_position_bridges:
            return ' │ '
        if Direction.right() in island.direction_position_bridges:
            return ' ──'
        if Direction.left() in island.direction_position_bridges:
            return '── '
        return ' X '
