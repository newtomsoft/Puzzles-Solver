import uuid
from typing import Collection

from z3 import Solver, Int, sat, And, Not, Or

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NanroSolver(GameSolver):
    no_filled_value = 0

    def __init__(self, values_grid: Grid, regions_grid: Grid):
        self._values_grid = values_grid
        self._regions_positions_by_id = regions_grid.get_regions()
        self.rows_number = self._values_grid.rows_number
        self.columns_number = self._values_grid.columns_number
        self._grid_z3: Grid | None = None
        self._solver = Solver()
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_values_cells_connected()
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        previous_solution_constraints = []
        for position, value in [(position, value) for (position, value) in self._previous_solution if value > self.no_filled_value]:
            previous_solution_constraints.append(self._grid_z3[position] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

        return self.get_solution()

    def _ensure_all_values_cells_connected(self):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            grid_bool = Grid([[model.eval(self._grid_z3.value(i, j)).as_long() != self.no_filled_value for j in range(self.columns_number)] for i in range(self.rows_number)])
            connected_values = grid_bool.get_all_shapes(value=True)
            if len(connected_values) == 1:
                solution = Grid([[model.eval(self._grid_z3.value(i, j)).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
                return solution, proposition_count

            wrong_solution = Grid([[model.eval(self._grid_z3.value(i, j)).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
            to_exclude_constraints = []
            for position, value in [(position, value) for position, value in wrong_solution]:
                to_exclude_constraints.append(self._grid_z3[position] == value)
            self._solver.add(Not(And(to_exclude_constraints)))

        return Grid.empty(), proposition_count

    def _add_constraints(self):
        self._add_initial_values_constraints()
        self._add_no_square_values_constraints()
        self._add_no_adjacents_same_values_with_other_regions__constraints()
        self._add_values_by_region_constraints()

    def _add_initial_values_constraints(self):
        for position, value in [(position, value) for (position, value) in self._values_grid if value != self.no_filled_value]:
            self._solver.add(self._grid_z3[position] == value)

    def _add_no_square_values_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                self._solver.add(
                    Not(And(self._grid_z3[r][c] != self.no_filled_value, self._grid_z3[r + 1][c] != self.no_filled_value, self._grid_z3[r][c + 1] != self.no_filled_value,
                            self._grid_z3[r + 1][c + 1] != self.no_filled_value)))

    def _add_values_by_region_constraints(self):
        for region_positions in self._regions_positions_by_id.values():
            self._add_same_values_or_empty_constraints(list(region_positions))
            self._add_count_values(region_positions)

    def _add_same_values_or_empty_constraints(self, positions: list[Position]):
        value = max([self._values_grid[position] for position in positions])
        if value != self.no_filled_value:
            for position in positions:
                self._solver.add(Or(self._grid_z3[position] == value, self._grid_z3[position] == self.no_filled_value))
        else:
            region_list = list(positions)
            for index, position in enumerate(region_list[:-2]):
                for next_position in region_list[index + 1:]:
                    self._solver.add(Or(self._grid_z3[position] == self._grid_z3[next_position], self._grid_z3[position] * self._grid_z3[next_position] == self.no_filled_value))

    def _add_count_values(self, positions: Collection[Position]):
        values_z3 = [self._grid_z3[position] for position in positions]
        self._solver.add(And([Or(value_z3 == self.no_filled_value, value_z3 > 0) for value_z3 in values_z3]))
        region_value = max([self._values_grid[position] for position in positions])
        if region_value != self.no_filled_value:
            self._solver.add(sum([value_z3 == region_value for value_z3 in values_z3]) == region_value)
        else:
            region_value_z3 = Int(f"value_region{uuid.uuid1()}")
            self._solver.add(And([region_value_z3 >= value_z3 for value_z3 in values_z3]))
            self._solver.add(Or([region_value_z3 == value_z3 for value_z3 in values_z3]))
            self._solver.add(sum([value_z3 == region_value_z3 for value_z3 in values_z3]) == region_value_z3)

    def _add_no_adjacents_same_values_with_other_regions__constraints(self):
        for region_positions in self._regions_positions_by_id.values():
            self._add_no_adjacents_same_value_with_other_regions_constraints(region_positions)

    def _add_no_adjacents_same_value_with_other_regions_constraints(self, region_positions: Collection[Position]):
        for position in region_positions:
            for neighbor_pos in [neighbor_position for neighbor_position in self._grid_z3.neighbors_positions(position) if neighbor_position not in region_positions]:
                self._solver.add(Or(self._grid_z3[position] != self._grid_z3[neighbor_pos], self._grid_z3[position] == self.no_filled_value, neighbor_pos == self.no_filled_value))
