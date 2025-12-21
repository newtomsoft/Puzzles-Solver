from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class DominosaSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 2 or self.columns_number < 3:
            raise ValueError("The grid must be at least 2x3")
        if self.columns_number != self.rows_number + 1:
            raise ValueError("The grid must be RxC with C = R + 1")
        self.dominoes_count = self.rows_number * self.columns_number // 2
        self.min_number_on_domino = min(self._grid.value(r, c) for r in range(self.rows_number) for c in range(self.columns_number))
        self.max_number_on_domino = max(self._grid.value(r, c) for r in range(self.rows_number) for c in range(self.columns_number))
        self.len_range_number_on_domino = self.rows_number
        if self.max_number_on_domino - self.min_number_on_domino + 1 != self.len_range_number_on_domino:
            raise ValueError(f"Values on dominoes must be between x and x + {self.len_range_number_on_domino - 1}")
        self._model = None
        self._solver = cp_model.CpSolver()
        self._dominoes_positions = None
        self._domino_position_bool_vars = None
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._dominoes_positions = {
            (value0, value1): [(self._model.NewIntVar(0, self.rows_number - 1, f"{value0}_{value1}_r0"), 
                               self._model.NewIntVar(0, self.columns_number - 1, f"{value0}_{value1}_c0")), 
                              (self._model.NewIntVar(0, self.rows_number - 1, f"{value0}_{value1}_r1"), 
                               self._model.NewIntVar(0, self.columns_number - 1, f"{value0}_{value1}_c1"))]
            for value0 in range(self.min_number_on_domino, self.max_number_on_domino + 1)
            for value1 in range(self.min_number_on_domino, value0 + 1)
        }
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.Solve(self._model)
        if self._status != cp_model.OPTIMAL and self._status != cp_model.FEASIBLE:
            return Grid.empty()

        return self._compute_solution()

    def _compute_solution(self):
        dominoes_positions = {
            (value0, value1): [Position(self._solver.Value(r), self._solver.Value(c)) for r, c in positions]
            for (value0, value1), positions in self._dominoes_positions.items()
        }
        solution_grid = Grid([[0 for _ in range(self.columns_number)] for _ in range(self.rows_number)])
        for _, positions in dominoes_positions.items():
            solution_grid[positions[0]] = positions[0].direction_to(positions[1])
            solution_grid[positions[1]] = positions[1].direction_to(positions[0])

        return solution_grid

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self.get_solution()

        if self._domino_position_bool_vars:
             constraints = []
             for domino_values, vars_positions in self._domino_position_bool_vars.items():
                 for bool_var, _, _ in vars_positions:
                     if self._solver.BooleanValue(bool_var):
                         constraints.append(bool_var.Not())
                     else:
                         constraints.append(bool_var)
             self._model.AddBoolOr(constraints)

        self._status = self._solver.Solve(self._model)
        if self._status != cp_model.OPTIMAL and self._status != cp_model.FEASIBLE:
            return Grid.empty()

        return self._compute_solution()

    def _add_constraints(self):
        self._dominoes_constraints()

    def _dominoes_constraints(self):
        possibles_dominoes_positions_by_value = self._get_all_possible_domino_positions_by_value()
        possibles_dominoes_positions_by_value = self.set_dominoes_positions_when_1_possibility_by_value(possibles_dominoes_positions_by_value)

        self._domino_position_bool_vars = {}
        for domino_values, possible_positions in possibles_dominoes_positions_by_value.items():
            self._domino_position_bool_vars[domino_values] = []
            for i, ((r0, c0), (r1, c1)) in enumerate(possible_positions):
                bool_var = self._model.NewBoolVar(f"domino_{domino_values[0]}_{domino_values[1]}_pos_{i}")
                self._domino_position_bool_vars[domino_values].append((bool_var, (r0, c0), (r1, c1)))

        for domino_values, vars_positions in self._domino_position_bool_vars.items():
            self._model.AddExactlyOne([var for var, _, _ in vars_positions])

        cell_usage = {}
        for domino_values, vars_positions in self._domino_position_bool_vars.items():
            for bool_var, (r0, c0), (r1, c1) in vars_positions:
                if (r0, c0) not in cell_usage:
                    cell_usage[(r0, c0)] = []
                if (r1, c1) not in cell_usage:
                    cell_usage[(r1, c1)] = []
                cell_usage[(r0, c0)].append(bool_var)
                cell_usage[(r1, c1)].append(bool_var)

        for cell, bool_vars in cell_usage.items():
            self._model.AddAtMostOne(bool_vars)

        for domino_values, vars_positions in self._domino_position_bool_vars.items():
            r0, c0 = self._dominoes_positions[domino_values][0]
            r1, c1 = self._dominoes_positions[domino_values][1]

            for bool_var, (pos_r0, pos_c0), (pos_r1, pos_c1) in vars_positions:
                self._model.Add(r0 == pos_r0).OnlyEnforceIf(bool_var)
                self._model.Add(c0 == pos_c0).OnlyEnforceIf(bool_var)
                self._model.Add(r1 == pos_r1).OnlyEnforceIf(bool_var)
                self._model.Add(c1 == pos_c1).OnlyEnforceIf(bool_var)

    def _get_all_possible_domino_positions_by_value(self):
        directions = [(0, 1), (1, 0)]
        possible_domino_positions = {
            (value0, value1): []
            for value0 in range(self.min_number_on_domino, self.max_number_on_domino + 1)
            for value1 in range(self.min_number_on_domino, value0 + 1)
        }
        for r0 in range(self.rows_number):
            for c0 in range(self.columns_number):
                domino_value_0: int = self._grid.value(r0, c0)
                for dr, dc in directions:
                    r1, c1 = r0 + dr, c0 + dc
                    if 0 <= r1 < self.rows_number and 0 <= c1 < self.columns_number:
                        domino_value_1: int = self._grid.value(r1, c1)
                        value_max, value_min = (max(domino_value_0, domino_value_1), min(domino_value_0, domino_value_1))
                        possible_domino_positions[value_max, value_min].append([(r0, c0), (r1, c1)])
        return possible_domino_positions

    def set_dominoes_positions_when_1_possibility_by_value(self, possibles_dominoes_positions_by_value):
        possibles_neighbors = {
            (r, c): {(r + dr, c + dc) for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)] if 0 <= r + dr < self.rows_number and 0 <= c + dc < self.columns_number}
            for r in range(self.rows_number)
            for c in range(self.columns_number)
        }
        to_set = True
        while to_set:
            to_set = False
            for domino_value_0, domino_value_1 in list(possibles_dominoes_positions_by_value.keys()):
                if len(possibles_dominoes_positions_by_value[(domino_value_0, domino_value_1)]) == 1:
                    to_set = True
                    (r0, c0), (r1, c1) = possibles_dominoes_positions_by_value[(domino_value_0, domino_value_1)][0]
                    r0_var, c0_var = self._dominoes_positions[(domino_value_0, domino_value_1)][0]
                    r1_var, c1_var = self._dominoes_positions[(domino_value_0, domino_value_1)][1]
                    self._model.Add(r0_var == r0)
                    self._model.Add(c0_var == c0)
                    self._model.Add(r1_var == r1)
                    self._model.Add(c1_var == c1)

                    possibles_neighbors = self._remove_position_from_possibles_neighbors((r0, c0), possibles_neighbors)
                    possibles_neighbors = self._remove_position_from_possibles_neighbors((r1, c1), possibles_neighbors)

                    possibles_dominoes_positions_by_value = {
                        key: [positions for positions in positions_list if (r0, c0) not in positions and (r1, c1) not in positions]
                        for key, positions_list in possibles_dominoes_positions_by_value.items() if key != (domino_value_0, domino_value_1)
                    }

            isolated_positions = {
                ((r0, c0), next(iter(possibles_neighbors[(r0, c0)])))
                for r0 in range(self.rows_number)
                for c0 in range(self.columns_number)
                if len(possibles_neighbors[(r0, c0)]) == 1
            }

            if isolated_positions:
                to_set = True
                for isolated_position in isolated_positions:
                    positions = list(isolated_position)
                    domino_value_0 = self._grid.value(positions[0][0], positions[0][1])
                    domino_value_1 = self._grid.value(positions[1][0], positions[1][1])
                    domino_values = (max(domino_value_0, domino_value_1), min(domino_value_0, domino_value_1))
                    possibles_dominoes_positions_by_value[domino_values] = [positions]

        return possibles_dominoes_positions_by_value

    @staticmethod
    def _remove_position_from_possibles_neighbors(position, possibles_neighbors):
        [possibles_neighbors[neighbor].remove(position) for neighbor in possibles_neighbors[position]]
        possibles_neighbors[position].clear()
        return possibles_neighbors
