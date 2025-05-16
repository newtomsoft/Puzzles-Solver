from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class AquariumSolver(GameSolver):
    def __init__(self, grid: Grid, numbers: list[int]):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")
        self._aquariums = self._grid.get_regions()
        if len(self._aquariums) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._numbers = numbers
        self.columns_water_numbers = numbers[:grid.rows_number]
        self.rows_water_numbers = numbers[grid.rows_number:]
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = None
        self._previous_solution = None

    def get_solution(self) -> Grid:
        self._grid_vars = Grid([[self._model.NewBoolVar(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        previous_solution_literals = []
        for position, value in self._previous_solution:
            temp_var = self._model.NewBoolVar(f"prev_{position.r}_{position.c}")
            self._model.Add(self._grid_vars[position] == value).OnlyEnforceIf(temp_var)
            self._model.Add(self._grid_vars[position] != value).OnlyEnforceIf(temp_var.Not())
            previous_solution_literals.append(temp_var)

        if previous_solution_literals:
            self._model.AddBoolOr([lit.Not() for lit in previous_solution_literals])

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        status = self._solver.Solve(self._model)
        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            return Grid.empty()

        grid = Grid([[self._solver.Value(self._grid_vars[Position(i, j)]) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_sum_constraints()
        self._add_aquariums_constraints()

    def _add_sum_constraints(self):
        for i, row in enumerate(self._grid_vars.matrix):
            self._model.Add(sum(row) == self.rows_water_numbers[i])

        for i in range(self.columns_number):
            column_vars = [self._grid_vars[Position(r, i)] for r in range(self.rows_number)]
            self._model.Add(sum(column_vars) == self.columns_water_numbers[i])

    def _add_aquariums_constraints(self):
        for positions in self._aquariums.values():
            cells_by_row_index = {}
            for position in positions:
                r, c = position
                if r not in cells_by_row_index:
                    cells_by_row_index[r] = []
                cells_by_row_index[r].append(position)

            for aquarium_row_cells in cells_by_row_index.values():
                if len(positions) > 1:
                    first_cell = aquarium_row_cells[0]
                    for cell in aquarium_row_cells[1:]:
                        self._model.Add(self._grid_vars[first_cell] == self._grid_vars[cell])

                row = aquarium_row_cells[0][0]
                column = aquarium_row_cells[0][1]
                cell_var = self._grid_vars[Position(row, column)]

                down_cells = [position for position in positions if position[0] > row]
                for down_cell in down_cells:
                    down_cell_var = self._grid_vars[down_cell]
                    self._model.AddImplication(cell_var, down_cell_var)

                up_cells = [position for position in positions if position[0] < row]
                for up_cell in up_cells:
                    up_cell_var = self._grid_vars[up_cell]
                    not_cell_var = self._model.NewBoolVar(f"not_cell_{row}_{column}")
                    self._model.AddBoolXOr([cell_var, not_cell_var])
                    self._model.AddImplication(not_cell_var, up_cell_var.Not())
