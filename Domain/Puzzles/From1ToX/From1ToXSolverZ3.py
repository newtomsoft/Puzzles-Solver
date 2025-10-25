from z3 import Solver, Not, And, unsat, Int, Distinct, Sum

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

_ = 0


class From1ToXSolver(GameSolver):
    def __init__(self, grid: Grid, region_grid: Grid, rows_clues: list, columns_clues: list):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._rows_clues = rows_clues
        self._columns_clues = columns_clues
        self._region_grid = region_grid
        self._regions = self._region_grid.get_regions()
        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[(model.eval(self._grid_z3[Position(i, j)])).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_initial_constraints()
        self._add_regions_distinct_and_max_value_constraints()
        self._add_clues_constraints()

    def _add_initial_constraints(self):
        for grid_z3_value, number_value in [(self._grid_z3[position], number_value) for position, number_value in self._grid]:
            if number_value != _:
                self._solver.add(grid_z3_value == number_value)
            else:
                self._solver.add(grid_z3_value >= 1)

    def _add_regions_distinct_and_max_value_constraints(self):
        for region_positions in self._regions.values():
            self._solver.add(Distinct([self._grid_z3[position] for position in region_positions]))
            for position in region_positions:
                self._add_max_value_constraints(position, len(region_positions))
                self._add_neighbors_not_same_value_constraint(position)

    def _add_max_value_constraints(self, position, region_positions_len: int):
        self._solver.add(self._grid_z3[position] <= region_positions_len)

    def _add_neighbors_not_same_value_constraint(self, position):
        self._solver.add(
            And([self._grid_z3[neighbor_position] != self._grid_z3[position] for neighbor_position in self._grid.neighbors_positions(position, 'orthogonal')]))

    def _add_clues_constraints(self):
        for r in range(self.rows_number):
            if self._rows_clues[r] != _:
                self._solver.add(Sum([self._grid_z3[Position(r, c)] for c in range(self.columns_number)]) == self._rows_clues[r])

        for c in range(self.columns_number):
            if self._columns_clues[c] != _:
                self._solver.add(Sum([self._grid_z3[Position(r, c)] for r in range(self.rows_number)]) == self._columns_clues[c])
