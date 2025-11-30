from typing import Dict

from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class HashiSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_bridges: Dict[Position, Dict[Direction, any]] = {}
        self._previous_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), self._input_grid[Position(r, c)]) if isinstance(self._input_grid[Position(r, c)], int) else None for c in range(self._input_grid.columns_number)] for r in range(self._input_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges = {
            island.position: {direction: self._model.NewIntVar(0, 2, f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()} for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._model.Proto().constraints:
            self._init_solver()

        solution, _ = self.get_grid_when_shape_is_loop()
        self._previous_solution = solution
        return solution

    def get_grid_when_shape_is_loop(self):
        proposition_count = 0
        status = self._solver.Solve(self._model)

        while status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            proposition_count += 1
            self.init_island_grid()

            for position, direction_bridges in self._island_bridges.items():
                for direction, bridges_var in direction_bridges.items():
                    bridges_number = self._solver.Value(bridges_var)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)

            self._previous_solution = self._island_grid
            connected_positions = self._island_grid.get_connected_positions()
            if len(connected_positions) == 1:
                return self._island_grid, proposition_count

            exclusion_literals = []
            for island in self._previous_solution.islands.values():
                for direction, (_, value) in island.direction_position_bridges.items():
                    temp_var = self._model.NewBoolVar(f"excl_{island.position}_{direction}")
                    self._model.Add(self._island_bridges[island.position][direction] == value).OnlyEnforceIf(temp_var)
                    self._model.Add(self._island_bridges[island.position][direction] != value).OnlyEnforceIf(temp_var.Not())
                    exclusion_literals.append(temp_var)

            if exclusion_literals:
                self._model.AddBoolOr([lit.Not() for lit in exclusion_literals])

            status = self._solver.Solve(self._model)

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        if self._previous_solution is None:
            return Grid.empty()

        exclusion_literals = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                temp_var = self._model.NewBoolVar(f"prev_{island.position}_{direction}")
                self._model.Add(self._island_bridges[island.position][direction] == value).OnlyEnforceIf(temp_var)
                self._model.Add(self._island_bridges[island.position][direction] != value).OnlyEnforceIf(temp_var.Not())
                exclusion_literals.append(temp_var)

        if exclusion_literals:
            self._model.AddBoolOr([lit.Not() for lit in exclusion_literals])

        self.init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_no_crossing_bridges_constraints()

    def _add_initial_constraints(self):
        for position, direction_bridges in self._island_bridges.items():
            bridge_vars = list(direction_bridges.values())
            self._model.Add(sum(bridge_vars) == self._island_grid[position].bridges_count)

        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is None:
                    self._model.Add(self._island_bridges[island.position][direction] == 0)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                opposite_direction = direction.opposite
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(self._island_bridges[island.position][direction] == 
                                   self._island_bridges[island.direction_position_bridges[direction][0]][opposite_direction])

    def _add_no_crossing_bridges_constraints(self):
        for possible_crossing_bridge in self._island_grid.possible_crossover_bridge:
            first_item, second_item = list(possible_crossing_bridge.items())[:2]
            first_position, first_direction = first_item
            second_position, second_direction = second_item

            first_has_bridge = self._model.NewBoolVar(f"first_{first_position}_{first_direction}")
            self._model.Add(self._island_bridges[first_position][first_direction] > 0).OnlyEnforceIf(first_has_bridge)
            self._model.Add(self._island_bridges[first_position][first_direction] == 0).OnlyEnforceIf(first_has_bridge.Not())
            self._model.Add(self._island_bridges[second_position][second_direction] == 0).OnlyEnforceIf(first_has_bridge)

            second_has_bridge = self._model.NewBoolVar(f"second_{second_position}_{second_direction}")
            self._model.Add(self._island_bridges[second_position][second_direction] > 0).OnlyEnforceIf(second_has_bridge)
            self._model.Add(self._island_bridges[second_position][second_direction] == 0).OnlyEnforceIf(second_has_bridge.Not())
            self._model.Add(self._island_bridges[first_position][first_direction] == 0).OnlyEnforceIf(second_has_bridge)
