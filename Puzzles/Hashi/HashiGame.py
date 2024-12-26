from typing import Dict

from z3 import Solver, sat, Int, And, Not, Distinct, Sum

from Puzzles.Hashi.Island import Island
from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.Position import Position


class HashiGame:
    def __init__(self, islands: Dict[Position, Island]):
        self._islands = islands
        self._solver: Solver | None = None
        self._island_bridges_z3: dict[Position: any] = {}
        self._last_solution: Grid | None = None

    def _init_solver(self):
        orthogonal_directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        self._island_bridges_z3 = {island.position: {Direction(direction): Int(f"{island.position}_{Direction(direction)}") for direction in orthogonal_directions} for island in self._islands.values()}
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> Dict[Position, Island]:
        if self._solver is None:
            self._init_solver()
        if self._solver.check() != sat:
            return {}
        model = self._solver.model()
        print()
        for position, direction_bridges in self._island_bridges_z3.items():
            for direction, bridges in direction_bridges.items():
                bridges_number = model.eval(bridges).as_long()
                if bridges_number > 0:
                    self._islands[position].set_bridge(self._islands[position].direction_position_bridges[direction][0], direction, bridges_number)
        self._last_solution = self._islands
        return self._islands

    def get_other_solution(self):
        exclusion_constraint = Not(And([True]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_no_crossing_bridges_constraints()

    def _add_initial_constraints(self):
        for position, direction_bridges in self._island_bridges_z3.items():
            self._solver.add(Sum(list(direction_bridges.values())) == self._islands[position].bridges)
            for bridges in direction_bridges.values():
                self._solver.add(bridges >= 0, bridges <= 2)

        for island in self._islands.values():
            for direction in [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]:
                if island.direction_position_bridges.get(direction) is None:
                    self._solver.add((self._island_bridges_z3[island.position][direction] == 0))

    def _add_opposite_bridges_constraints(self):
        for island in self._islands.values():
            for direction in [Direction(Direction.RIGHT), Direction(Direction.DOWN), Direction(Direction.LEFT), Direction(Direction.UP)]:
                opposite_direction = direction.opposite
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[island.direction_position_bridges[direction][0]][opposite_direction])

    def _add_no_crossing_bridges_constraints(self):
        pass
