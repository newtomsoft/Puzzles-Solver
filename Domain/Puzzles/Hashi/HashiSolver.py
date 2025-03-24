from typing import Dict

from Domain.Direction import Direction
from Domain.Grid.Grid import Grid
from Domain.Grid.IslandsGrid import IslandGrid
from Domain.Island import Island
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Position import Position
from GameSolver import GameSolver


class HashiSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._input_grid = grid
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._solver = solver_engine
        self._island_bridges_z3: Dict[Position, Dict[Direction, any]] = {}
        self._previous_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), self._input_grid[Position(r, c)]) if isinstance(self._input_grid[Position(r, c)], int) else None for c in range(self._input_grid.columns_number)] for r in range(self._input_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {direction: self._solver.int(f"{island.position}_{direction}") for direction in Direction.orthogonal()} for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.has_constraints():
            self._init_solver()

        solution, _ = self.get_grid_when_shape_is_loop()
        self._previous_solution = solution
        return solution

    def get_grid_when_shape_is_loop(self):
        proposition_count = 0
        while self._solver.has_solution():
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    bridges_number = self._solver.eval(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)

            self._previous_solution = self._island_grid
            connected_positions = self._island_grid.get_connected_positions()
            if len(connected_positions) == 1:
                return self._island_grid, proposition_count

            wrong_solution_constraints = []
            for island in self._previous_solution.islands.values():
                for direction, (_, value) in island.direction_position_bridges.items():
                    wrong_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
            self._solver.add(self._solver.Not(self._solver.And(wrong_solution_constraints)))
            self.init_island_grid()

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(self._solver.Not(self._solver.And(previous_solution_constraints)))

        self.init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_no_crossing_bridges_constraints()

    def _add_initial_constraints(self):
        for position, direction_bridges in self._island_bridges_z3.items():
            self._solver.add(self._solver.sum(list(direction_bridges.values())) == self._island_grid[position].bridges_count)
            for bridges in direction_bridges.values():
                self._solver.add(bridges >= 0)
                self._solver.add(bridges <= 2)

        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is None:
                    self._solver.add((self._island_bridges_z3[island.position][direction] == 0))

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                opposite_direction = direction.opposite
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[island.direction_position_bridges[direction][0]][opposite_direction])

    def _add_no_crossing_bridges_constraints(self):
        for possible_crossing_bridge in self._island_grid.possible_crossover_bridge:
            first_item, second_item = list(possible_crossing_bridge.items())[:2]
            first_position, first_direction = first_item
            second_position, second_direction = second_item
            self._solver.add(self._solver.Implies(self._island_bridges_z3[first_position][first_direction] > 0, self._island_bridges_z3[second_position][second_direction] == 0))
            self._solver.add(self._solver.Implies(self._island_bridges_z3[second_position][second_direction] > 0, self._island_bridges_z3[first_position][first_direction] == 0))
