from typing import Dict

from Utils.Direction import Direction
from Utils.Position import Position


class Island:
    _islands: Dict[Position, 'Island'] = {}

    def __init__(self, position: Position, bridges: int):
        self.position = position
        self.bridges = bridges
        if bridges < 1 or bridges > 8:
            raise ValueError("Bridges must be between 1 and 8")
        Island._islands[position] = self
        self.direction_position_bridges: Dict[Direction, (Position, int)] = {}
        self.compute_possible_bridges()

    def compute_possible_bridges(self):
        min_distances = {}
        for other_island in Island._islands.values():
            direction = self.position.direction_to(other_island.position)
            if direction != Direction.RIGHT and direction != Direction.LEFT and direction != Direction.UP and direction != Direction.DOWN:
                continue
            distance = other_island.position.distance_to(self.position)
            if direction == Direction.RIGHT and distance < min_distances.get(Direction.RIGHT, (float('inf'), None))[0]:
                min_distances[Direction.RIGHT] = (distance, other_island.position)
                continue
            if direction == Direction.LEFT and distance < min_distances.get(Direction.LEFT, (float('inf'), None))[0]:
                min_distances[Direction.LEFT] = (distance, other_island.position)
                continue
            if direction == Direction.UP and distance < min_distances.get(Direction.UP, (float('inf'), None))[0]:
                min_distances[Direction.UP] = (distance, other_island.position)
                continue
            if direction == Direction.DOWN and distance < min_distances.get(Direction.DOWN, (float('inf'), None))[0]:
                min_distances[Direction.DOWN] = (distance, other_island.position)
                continue
        if min_distances.get(Direction.RIGHT) is not None:
            self.direction_position_bridges[Direction.RIGHT] = min_distances[Direction.RIGHT][1], 0
            Island._islands[min_distances[Direction.RIGHT][1]].direction_position_bridges[Direction.LEFT] = self.position, 0
        if min_distances.get(Direction.LEFT) is not None:
            self.direction_position_bridges[Direction.LEFT] = min_distances[Direction.LEFT][1], 0
            Island._islands[min_distances[Direction.LEFT][1]].direction_position_bridges[Direction.RIGHT] = self.position, 0
        if min_distances.get(Direction.UP) is not None:
            self.direction_position_bridges[Direction.UP] = min_distances[Direction.UP][1], 0
            Island._islands[min_distances[Direction.UP][1]].direction_position_bridges[Direction.DOWN] = self.position, 0
        if min_distances.get(Direction.DOWN) is not None:
            self.direction_position_bridges[Direction.DOWN] = min_distances[Direction.DOWN][1], 0
            Island._islands[min_distances[Direction.DOWN][1]].direction_position_bridges[Direction.UP] = self.position, 0

    def set_bridge(self, position: Position, number: int):
        direction = self.position.direction_to(position)
        self.direction_position_bridges[direction] = position, number
        Island._islands[position].direction_position_bridges[direction.opposite] = self.position, number

    @classmethod
    def reset_all_bridges(cls):
        for island in cls._islands.values():
            for position, _ in island.direction_position_bridges.values():
                island.set_bridge(position, 0)

    def __eq__(self, other):
        return self.position == other.position and self.bridges == other.bridges and self.direction_position_bridges == other.direction_position_bridges

    def __repr__(self):
        return f"Island({self.position}, {self.bridges} {self.direction_position_bridges})"

    @classmethod
    def compute_possible_crossover_bridges(cls):
        for island in cls._islands.values():
            for direction, (position, number) in island.direction_position_bridges.items():
                pass