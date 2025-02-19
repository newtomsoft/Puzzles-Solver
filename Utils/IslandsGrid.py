from typing import Dict

from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.Island import Island
from Utils.Position import Position


class IslandGrid(Grid[Island]):
    def __init__(self, input_matrix: list[list[int | Island]]):
        super().__init__(input_matrix)
        self.islands: Dict[Position, Island] = {}
        for position, island_or_bridges_number in self:
            if isinstance(island_or_bridges_number, Island) and island_or_bridges_number.bridges_count != 0:
                self.islands[position] = island_or_bridges_number
            elif isinstance(island_or_bridges_number, int) and island_or_bridges_number != 0:
                self.islands[position] = Island(position, island_or_bridges_number)

        if len(self.islands) == 0:
            super().__init__([[]])
            self.islands = {}
            return

        self._compute_possible_bridges()
        self.possible_crossover_bridge = self._compute_possible_crossover_bridges()

    @staticmethod
    def empty() -> 'IslandGrid':
        return IslandGrid([[]])

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

    def get_connected_positions(self, exclude_without_bridge=False) -> list[set[Position]]:
        concerned_islands_count = len(self.islands) if not exclude_without_bridge else sum(1 for island in self.islands.values() if island.bridges_count != 0)
        visited_list: list[set[Position]] = []
        visited_flat: set[Position] = set()
        while len(visited_flat) != concerned_islands_count:
            position = next(island.position for island in self.islands.values() if island.position not in visited_flat) if not exclude_without_bridge else next(
                (island.position for island in self.islands.values() if island.bridges_count != 0 and island.position not in visited_flat), None)
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

    def __repr__(self) -> str:
        if self.is_empty():
            return 'IslandGrid.empty()'
        current_row = 0
        result = ''
        for position, island in self:
            if position.r != current_row:
                result += '\n'
                current_row = position.r
            if isinstance(island, Island):
                result += repr(island)
            else:
                result += self.get_str_new(position)
        return result

    def get_str_new(self, position: Position) -> str:
        island = Island(position, 0)
        for direction in Direction.orthogonal():
            iteration = 1
            while position.after(direction, iteration) in self:
                if position.after(direction, iteration) in self.islands.keys():
                    bridges_numbers = self.islands[position.after(direction, iteration)].bridges_number(direction.opposite)
                    island.set_bridge(position.after(direction, iteration), bridges_numbers)
                    break
                iteration += 1
        island.set_bridges_count_according_to_directions_bridges()
        island_repr = repr(island)
        return island_repr
