from itertools import combinations
from typing import Collection

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class BorderBlockSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid, dots: Collection[Position]):
        self._input_grid = grid
        self._dots = dots
        self._rows_number = self._input_grid.rows_number
        self._columns_number = self._input_grid.columns_number
        self._max_region_id = max((value for position, value in self._input_grid if value is not None), default=1)
        self._grid_vars = {}
        self._model = cp_model.CpModel()
        self._previous_solution: Grid = Grid.empty()

    def get_solution(self) -> Grid:
        self._model = cp_model.CpModel()
        self._grid_vars = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                self._grid_vars[Position(r, c)] = self._model.NewIntVar(1, self._max_region_id, f"region_id_{r}_{c}")

        self._add_constraints()

        solution, _ = self._ensure_all_shapes_compliant()
        self._previous_solution = solution
        return solution

    def _ensure_all_shapes_compliant(self) -> tuple[Grid, int]:
        solver = cp_model.CpSolver()
        proposition_count = 0

        while True:
            status = solver.Solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return Grid.empty(), proposition_count

            proposition_count += 1
            proposition_grid = Grid(
                [[solver.Value(self._grid_vars[Position(r, c)]) for c in range(self._columns_number)] for r in range(self._rows_number)])

            shapes = {circle_value: proposition_grid.get_all_shapes(circle_value) for circle_value in range(1, self._max_region_id + 1)}
            not_compliant_shapes = [(value, shapes_positions) for (value, shapes_positions) in shapes.items() if len(shapes_positions) > 1]

            if len(not_compliant_shapes) == 0:
                return proposition_grid, proposition_count

            for region_id, shapes_positions in not_compliant_shapes:
                positions = frozenset().union(*shapes_positions)

                literals = []

                for pos in positions:
                    if pos in self._grid_vars:
                        b_eq = self._model.NewBoolVar(f"eq_{pos}_{region_id}")
                        self._model.Add(self._grid_vars[pos] == region_id).OnlyEnforceIf(b_eq)
                        self._model.Add(self._grid_vars[pos] != region_id).OnlyEnforceIf(b_eq.Not())
                        literals.append(b_eq.Not())

                for pos in ShapeGenerator.around_shape(positions):
                    if pos in self._grid_vars:
                        b_eq = self._model.NewBoolVar(f"eq_{pos}_{region_id}")
                        self._model.Add(self._grid_vars[pos] == region_id).OnlyEnforceIf(b_eq)
                        self._model.Add(self._grid_vars[pos] != region_id).OnlyEnforceIf(b_eq.Not())
                        literals.append(b_eq)

                self._model.AddBoolOr(literals)

    def get_other_solution(self) -> Grid:
        literals = []
        for pos, val in self._previous_solution:
            if pos in self._grid_vars:
                b_eq = self._model.NewBoolVar(f"prev_eq_{pos}_{val}")
                self._model.Add(self._grid_vars[pos] == val).OnlyEnforceIf(b_eq)
                self._model.Add(self._grid_vars[pos] != val).OnlyEnforceIf(b_eq.Not())
                literals.append(b_eq.Not())

        self._model.AddBoolOr(literals)

        solution, _ = self._ensure_all_shapes_compliant()
        self._previous_solution = solution
        return solution

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_dots_constraints()
        self._add_not_dots_constraints()

    def _add_initials_constraints(self):
        for position, value in self._input_grid:
            if value is None:
                pass
            else:
                self._model.Add(self._grid_vars[position] == value)

    def _add_dots_constraints(self):
        for dot in self._dots:
            self._add_dot_constraint(dot)

    def _add_dot_constraint(self, dot: Position):
        neighbors_pos = [pos for pos in dot.straddled_neighbors() if pos in self._grid_vars]
        neighbors_vars = [self._grid_vars[pos] for pos in neighbors_pos]

        if self._add_edge_dot_constraints(neighbors_vars):
            return

        self._add_inside_dot_constraint(neighbors_vars)

    def _add_edge_dot_constraints(self, neighbors_vars: list[cp_model.IntVar]) -> bool:
        if len(neighbors_vars) == 2:
            self._model.Add(neighbors_vars[0] != neighbors_vars[1])
            return True
        return False

    def _add_inside_dot_constraint(self, neighbors_vars: list[cp_model.IntVar]):
        trios = list(combinations(range(4), 3))
        trio_bools = []

        pairs = list(combinations(range(4), 2))
        pair_eq_vars = {}

        for i, j in pairs:
            b_eq = self._model.NewBoolVar(f"eq_{neighbors_vars[i]}_{neighbors_vars[j]}")
            self._model.Add(neighbors_vars[i] == neighbors_vars[j]).OnlyEnforceIf(b_eq)
            self._model.Add(neighbors_vars[i] != neighbors_vars[j]).OnlyEnforceIf(b_eq.Not())
            pair_eq_vars[(i, j)] = b_eq
            pair_eq_vars[(j, i)] = b_eq

        for trio in trios:
            b_trio = self._model.NewBoolVar(f"distinct_trio_{trio}")

            self._model.AddImplication(b_trio, pair_eq_vars[(trio[0], trio[1])].Not())
            self._model.AddImplication(b_trio, pair_eq_vars[(trio[0], trio[2])].Not())
            self._model.AddImplication(b_trio, pair_eq_vars[(trio[1], trio[2])].Not())

            trio_bools.append(b_trio)

        self._model.AddBoolOr(trio_bools)

    def _add_not_dots_constraints(self):
        self._add_not_edge_dot_constraints()
        self._add_not_inside_dot_constraints()

    def _add_not_edge_dot_constraints(self):
        empty_border_positions = self._get_empty_border_positions()
        for position in empty_border_positions:
            neighbors_pos = [p for p in position.straddled_neighbors() if p in self._grid_vars]
            if len(neighbors_pos) >= 2:
                self._model.Add(self._grid_vars[neighbors_pos[0]] == self._grid_vars[neighbors_pos[1]])

    def _add_not_inside_dot_constraints(self):
        inside_positions = self._get_inside_positions()
        for position in inside_positions:
            neighbors_pos = position.straddled_neighbors()
            neighbors_vars = [self._grid_vars[p] for p in neighbors_pos if p in self._grid_vars]
            if len(neighbors_vars) < 4:
                continue

            v1 = self._model.NewIntVar(1, self._max_region_id, f"v1_{position}")
            v2 = self._model.NewIntVar(1, self._max_region_id, f"v2_{position}")

            for nv in neighbors_vars:
                b_v1 = self._model.NewBoolVar(f"{nv}_eq_v1")
                b_v2 = self._model.NewBoolVar(f"{nv}_eq_v2")

                self._model.Add(nv == v1).OnlyEnforceIf(b_v1)
                self._model.Add(nv != v1).OnlyEnforceIf(b_v1.Not())

                self._model.Add(nv == v2).OnlyEnforceIf(b_v2)
                self._model.Add(nv != v2).OnlyEnforceIf(b_v2.Not())

                self._model.AddBoolOr([b_v1, b_v2])

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
