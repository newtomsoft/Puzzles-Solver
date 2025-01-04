from typing import Dict, Tuple

from Utils.Direction import Direction
from Utils.Position import Position


class Island:
    def __init__(self, position: Position, bridges: int):
        self.position = position
        self.bridges = bridges
        if bridges < 1 or bridges > 8:
            raise ValueError("Bridges must be between 1 and 8")
        self.direction_position_bridges: Dict[Direction, Tuple[Position, int]] = {}

    def set_bridge(self, position: Position, number: int):
        direction = self.position.direction_to(position)
        self.direction_position_bridges[direction] = position, number

    def __eq__(self, other):
        return self.position == other.position and self.bridges == other.bridges and self.direction_position_bridges == other.direction_position_bridges

    def __repr__(self):
        return f"{self.bridges} ; {self.direction_position_bridges}"
