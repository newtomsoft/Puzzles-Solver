from typing import Any

from z3 import Bool, Solver, sat, is_true, Not, Implies, Or

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class AkariSolver(GameSolver):
    def __init__(self, data_game: dict[str, Any]):
        self._data_game = data_game
        self.rows_number = self._data_game['rows_number']
        self.columns_number = self._data_game['columns_number']
        self._black_cells = self._data_game['black_cells']
        self._number_constraints = self._data_game['number_constraints']

        if self.rows_number < 7 or self.columns_number < 7:
            raise ValueError("Akari grid must be at least 7x7")
        self._solver = Solver()
        self._illuminated_z3 = None
        self._bulbs_z3 = None

    def get_solution(self) -> Grid:
        self._bulbs_z3 = [[Bool(f'bulb_{r}_{c}') for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._illuminated_z3 = [[Bool(f'illuminated_{r}_{c}') for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()
        if not self._solver.check() == sat:
            return Grid.empty()

        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def _compute_solution(self) -> Grid:
        model = self._solver.model()
        solution = [[1 if is_true(model.eval(self._bulbs_z3[r][c])) else 0 for c in range(self.columns_number)] for r in range(self.rows_number)]
        return Grid(solution)

    def _add_constraints(self):
        self._add_numbers_constraints()
        self._add_black_cells_constraints()
        self._add_light_constraints()
        self._add_bulbs_constraints()

    def _add_numbers_constraints(self):
        for (current_row, current_column), number in self._number_constraints.items():
            adjacent_cells = [(current_row - 1, current_column), (current_row + 1, current_column), (current_row, current_column - 1), (current_row, current_column + 1)]
            adjacent_bulbs = [self._bulbs_z3[r][c] for r, c in adjacent_cells if 0 <= r < self.rows_number and 0 <= c < self.columns_number and (r, c) not in self._black_cells]
            constraint = sum([adjacent_bulb for adjacent_bulb in adjacent_bulbs]) == number
            self._solver.add(constraint)

    def _add_black_cells_constraints(self):
        for (i, j) in self._black_cells:
            self._solver.add(Not(self._bulbs_z3[i][j]))
            self._solver.add(Not(self._illuminated_z3[i][j]))

    def _add_light_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if (r, c) in self._black_cells:
                    continue
                light_constraints = [self._bulbs_z3[r][c]]
                for r1 in range(r - 1, -1, -1):
                    if (r1, c) in self._black_cells:
                        break
                    light_constraints.append(self._bulbs_z3[r1][c])
                for r1 in range(r + 1, self.rows_number):
                    if (r1, c) in self._black_cells:
                        break
                    light_constraints.append(self._bulbs_z3[r1][c])
                for c1 in range(c - 1, -1, -1):
                    if (r, c1) in self._black_cells:
                        break
                    light_constraints.append(self._bulbs_z3[r][c1])
                for c1 in range(c + 1, self.columns_number):
                    if (r, c1) in self._black_cells:
                        break
                    light_constraints.append(self._bulbs_z3[r][c1])
                constraint = self._illuminated_z3[r][c] == Or(light_constraints)
                self._solver.add(constraint)
                self._solver.add(self._illuminated_z3[r][c])

    def _add_bulbs_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if (r, c) not in self._black_cells:
                    constraints = []
                    for r1 in range(r - 1, -1, -1):
                        if (r1, c) in self._black_cells:
                            break
                        constraints.append(Implies(self._bulbs_z3[r][c], Not(self._bulbs_z3[r1][c])))
                    for r1 in range(r + 1, self.rows_number):
                        if (r1, c) in self._black_cells:
                            break
                        constraints.append(Implies(self._bulbs_z3[r][c], Not(self._bulbs_z3[r1][c])))
                    for c1 in range(c - 1, -1, -1):
                        if (r, c1) in self._black_cells:
                            break
                        constraints.append(Implies(self._bulbs_z3[r][c], Not(self._bulbs_z3[r][c1])))
                    for c1 in range(c + 1, self.columns_number):
                        if (r, c1) in self._black_cells:
                            break
                        constraints.append(Implies(self._bulbs_z3[r][c], Not(self._bulbs_z3[r][c1])))
                    self._solver.add(constraints)
