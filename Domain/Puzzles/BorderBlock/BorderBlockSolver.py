from itertools import combinations
from typing import Collection

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class BorderBlockSolver(GameSolver):
    cell_empty = None

    def __init__(self, grid: Grid, dots: Collection[Position]):
        self._input_grid = grid
        self._dots = set(dots)
        self._rows_number = self._input_grid.rows_number
        self._columns_number = self._input_grid.columns_number
        self._max_region_id = max(value for position, value in self._input_grid if value is not None)
        self._cell_vars: list[list] = []
        self._rank_vars: list[list] = []
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._previous_solution: Grid = Grid.empty()
        self._initialized = False

    def _init_solver(self):
        self._cell_vars = [
            [self._model.NewIntVar(1, self._max_region_id, f"region_id_{r}_{c}") for c in range(self._columns_number)]
            for r in range(self._rows_number)
        ]
        self._add_constraints()
        self._initialized = True

    def get_solution(self) -> Grid:
        if not self._initialized:
            self._init_solver()

        status = self._solver.Solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = Grid([
            [self._solver.Value(self._cell_vars[r][c]) for c in range(self._columns_number)]
            for r in range(self._rows_number)
        ])
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution.is_empty():
            return self.get_solution()

        block_literals = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                b = self._model.NewBoolVar(f"block_{r}_{c}")
                self._model.Add(self._cell_vars[r][c] != self._previous_solution[r][c]).OnlyEnforceIf(b)
                block_literals.append(b)
        self._model.AddBoolOr(block_literals)

        return self.get_solution()

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_dots_constraints()
        self._add_not_dots_constraints()
        self._add_region_connectivity_constraints()

    def _add_region_connectivity_constraints(self):
        total_cells = self._rows_number * self._columns_number
        self._rank_vars = [
            [self._model.NewIntVar(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self._columns_number)]
            for r in range(self._rows_number)
        ]

        for region_id in range(1, self._max_region_id + 1):
            is_root_vars = []
            in_region_list = []

            for r in range(self._rows_number):
                for c in range(self._columns_number):
                    is_root = self._model.NewBoolVar(f"root_{region_id}_{r}_{c}")
                    is_root_vars.append(is_root)

                    in_region = self._model.NewBoolVar(f"in_region_{region_id}_{r}_{c}")
                    in_region_list.append(in_region)
                    self._model.Add(self._cell_vars[r][c] == region_id).OnlyEnforceIf(in_region)
                    self._model.Add(self._cell_vars[r][c] != region_id).OnlyEnforceIf(in_region.Not())

                    self._model.Add(self._rank_vars[r][c] == 0).OnlyEnforceIf(is_root)
                    self._model.Add(is_root <= in_region)

                    parent_literals = []
                    pos = Position(r, c)
                    for neighbor in self._input_grid.neighbors_positions(pos):
                        n_in_region = self._model.NewBoolVar(f"n_in_region_{region_id}_{r}_{c}_{neighbor.r}_{neighbor.c}")
                        self._model.Add(self._cell_vars[neighbor.r][neighbor.c] == region_id).OnlyEnforceIf(n_in_region)
                        self._model.Add(self._cell_vars[neighbor.r][neighbor.c] != region_id).OnlyEnforceIf(n_in_region.Not())

                        parent = self._model.NewBoolVar(f"parent_{region_id}_{r}_{c}_{neighbor.r}_{neighbor.c}")
                        self._model.Add(parent <= n_in_region)
                        self._model.Add(self._rank_vars[neighbor.r][neighbor.c] < self._rank_vars[r][c]).OnlyEnforceIf(parent)
                        parent_literals.append(parent)

                    if parent_literals:
                        self._model.AddBoolOr(parent_literals).OnlyEnforceIf([in_region, is_root.Not()])

            region_exists = self._model.NewBoolVar(f"region_exists_{region_id}")
            self._model.AddBoolOr(in_region_list).OnlyEnforceIf(region_exists)
            for ir in in_region_list:
                self._model.AddImplication(ir, region_exists)

            root_sum = sum(is_root_vars)
            self._model.Add(root_sum == 1).OnlyEnforceIf(region_exists)
            self._model.Add(root_sum == 0).OnlyEnforceIf(region_exists.Not())

    def _add_initials_constraints(self):
        for position, value in self._input_grid:
            cell_var = self._cell_vars[position.r][position.c]
            if value is None:
                self._model.Add(cell_var >= 1)
                self._model.Add(cell_var <= self._max_region_id)
            else:
                self._model.Add(cell_var == value)

    def _add_dots_constraints(self):
        for dot in self._dots:
            self._add_dot_constraint(dot)

    def _add_dot_constraint(self, dot: Position):
        neighbors_value = [self._cell_vars[position.r][position.c] for position in dot.straddled_neighbors() if position in self._input_grid]
        if self._add_edge_dot_constraints(neighbors_value):
            return
        self._add_inside_dot_constraint(dot, neighbors_value)

    def _add_edge_dot_constraints(self, neighbors_value) -> bool:
        if len(neighbors_value) == 2:
            self._model.Add(neighbors_value[0] != neighbors_value[1])
            return True
        return False

    def _add_inside_dot_constraint(self, dot: Position, neighbors_value):
        trios = list(combinations(range(len(neighbors_value)), 3))
        is_all_diff = [self._model.NewBoolVar(f"all_diff_{int(dot.r * 2)}_{int(dot.c * 2)}_{i}") for i in range(len(trios))]
        for i, idx_trio in enumerate(trios):
            trio_vars = [neighbors_value[j] for j in idx_trio]
            self._model.AddAllDifferent(trio_vars).OnlyEnforceIf(is_all_diff[i])
        self._model.AddBoolOr(is_all_diff)

    def _add_not_dots_constraints(self):
        self._add_not_edge_dot_constraints()
        self._add_not_inside_dot_constraints()

    def _add_not_edge_dot_constraints(self):
        empty_border_positions = self._get_empty_border_positions()
        for position in empty_border_positions:
            neighbors_value = [self._cell_vars[neighbor.r][neighbor.c] for neighbor in position.straddled_neighbors() if neighbor in self._input_grid]
            self._model.Add(neighbors_value[0] == neighbors_value[1])

    def _add_not_inside_dot_constraints(self):
        inside_positions = self._get_inside_positions()
        for position in inside_positions:
            v1 = self._model.NewIntVar(1, self._max_region_id, f"v1_{int(position.r * 2)}_{int(position.c * 2)}")
            v2 = self._model.NewIntVar(1, self._max_region_id, f"v2_{int(position.r * 2)}_{int(position.c * 2)}")
            neighbors_value = [self._cell_vars[neighbor.r][neighbor.c] for neighbor in position.straddled_neighbors()]
            for i, nv in enumerate(neighbors_value):
                eq_v1 = self._model.NewBoolVar(f"eq_v1_{int(position.r * 2)}_{int(position.c * 2)}_{i}")
                eq_v2 = self._model.NewBoolVar(f"eq_v2_{int(position.r * 2)}_{int(position.c * 2)}_{i}")
                self._model.Add(nv == v1).OnlyEnforceIf(eq_v1)
                self._model.Add(nv == v2).OnlyEnforceIf(eq_v2)
                self._model.AddBoolOr([eq_v1, eq_v2])

    def _get_empty_border_positions(self) -> set[Position]:
        first_position = Position(-0.5, -0.5)
        positions = set()
        for c in range(1, self._columns_number):
            positions.add(first_position + Position(0, c))
            positions.add(first_position + Position(self._rows_number, c))

        for r in range(1, self._rows_number):
            positions.add(first_position + Position(r, 0))
            positions.add(first_position + Position(r, self._columns_number))

        positions -= set(self._dots)
        return positions

    def _get_inside_positions(self):
        first_position = Position(-0.5, -0.5)
        positions = set()
        for r in range(1, self._rows_number):
            for c in range(1, self._columns_number):
                positions.add(first_position + Position(r, c))

        positions -= set(self._dots)
        return positions
