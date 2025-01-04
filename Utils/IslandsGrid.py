from typing import Dict

from Puzzles.Hashi.Island import Island
from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.Position import Position


class IslandGrid(Grid):
    def __init__(self, grid: Grid):
        self.islands = {}
        for position, bridges in grid:
            if bridges != 0:
                self.islands[position] = Island(position, bridges)

        if len(self.islands) == 0:
            super().__init__([[]])
            self.islands = {}
            return

        matrix = [[self.islands[position] if (position := Position(r, c)) in self.islands.keys() else 0 for c in range(grid.columns_number + 1)] for r in range(grid.rows_number + 1)]
        super().__init__(matrix)
        self._compute_possible_bridges()
        self.possible_crossover_bridge = self._compute_possible_crossover_bridges()

    @staticmethod
    def empty() -> 'IslandGrid':
        return IslandGrid({})

    def get_island(self, position: Position) -> Island:
        return self.islands[position] if position in self.islands.keys() else 0

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

    def reset_all_bridges(self):
        for island in self.islands.values():
            for position, _ in island.direction_position_bridges.values():
                island.set_bridge(position, 0)

    def __str__(self) -> str:
        return '\n'.join(' '.join(str(self.string(cell)) for cell in row) for row in self._matrix)

    def __repr__(self) -> str:
        if self.is_empty():
            return 'Grid.empty()'
        return self.__str__()

    @staticmethod
    def string(cell: Island | int) -> str:
        if isinstance(cell, Island):
            return str(cell.direction_position_bridges)
        return ' '
