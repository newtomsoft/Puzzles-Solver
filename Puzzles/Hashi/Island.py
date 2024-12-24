from Utils.Direction import Direction
from Utils.Position import Position


class Island:
    _islands: {Position: 'Island'} = {}

    def __init__(self, position: Position, links_number: int):
        self.position = position
        self.links_number = links_number
        if links_number < 1 or links_number > 8:
            raise ValueError("Links number must be between 1 and 8")
        Island._islands[position] = self
        self.direction_islands_links_number: {Direction: (Position, int)} = {}
        self.compute_possible_links()

    def compute_possible_links(self):
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
            self.direction_islands_links_number[Direction.RIGHT] = min_distances[Direction.RIGHT][1], 0
            Island._islands[min_distances[Direction.RIGHT][1]].direction_islands_links_number[Direction.LEFT] = self.position, 0
        if min_distances.get(Direction.LEFT) is not None:
            self.direction_islands_links_number[Direction.LEFT] = min_distances[Direction.LEFT][1], 0
            Island._islands[min_distances[Direction.LEFT][1]].direction_islands_links_number[Direction.RIGHT] = self.position, 0
        if min_distances.get(Direction.UP) is not None:
            self.direction_islands_links_number[Direction.UP] = min_distances[Direction.UP][1], 0
            Island._islands[min_distances[Direction.UP][1]].direction_islands_links_number[Direction.DOWN] = self.position, 0
        if min_distances.get(Direction.DOWN) is not None:
            self.direction_islands_links_number[Direction.DOWN] = min_distances[Direction.DOWN][1], 0
            Island._islands[min_distances[Direction.DOWN][1]].direction_islands_links_number[Direction.UP] = self.position, 0
