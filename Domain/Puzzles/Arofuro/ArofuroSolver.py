from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpSolver

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class ArofuroSolver(GameSolver):
    Empty = None
    Black = 'B'
    up = 1
    down = 2
    right = 3
    left = 4

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars = Grid.empty()
        self._region_id_vars = Grid.empty()
        self._rank_vars = Grid.empty()
        self._previous_solution = Grid.empty()
        self._solver: CpSolver | None = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.NewIntVar(0, 4, f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])

        self._rank_vars = Grid(
            [[self._model.NewIntVar(0, self._rows_number * self._columns_number, f"rank_{r}_{c}") for c in range(self._columns_number)] for r in
             range(self._rows_number)])

        self.value_by_region_id = {}
        self._region_id_by_position = {}
        for index, (position, val) in enumerate([(position, val) for position, val in self._grid if val not in {self.Black, self.Empty}]):
            self.value_by_region_id[index] = val
            self._region_id_by_position[position] = index

        self._region_id_vars = Grid(
            [[self._model.NewIntVar(-1, max(self._region_id_by_position.values()), f"region_{r}_{c}") for c in range(self._columns_number)] for r in
             range(self._rows_number)])

        self._add_constraints()

    def solution_to_string(self) -> str:
        value_by_arrow = {0: '•', 1: '↑', 2: '↓', 3: '→', 4: '←'}
        if self._solver is None:
            self.get_solution()

        if self._previous_solution == Grid.empty():
            return "No solution found"

        grid_str = ""
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                grid_str += value_by_arrow[self._previous_solution[r][c]] + " "
            grid_str += "\n"

        return grid_str.strip('\n')

    def get_solution(self) -> Grid:
        self._init_solver()

        self._solver = cp_model.CpSolver()
        status = self._solver.Solve(self._model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution_grid = Grid([[self._solver.Value(self._grid_vars[r][c]) for c in range(self._columns_number)] for r in range(self._rows_number)])
            self._previous_solution = solution_grid
            return solution_grid
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution == Grid.empty():
            return self.get_solution()

        negated_constraints_bools = []
        for position, _ in self._grid:
            if self._previous_solution[position] != 0:  # Only constrain arrows
                b = self._model.NewBoolVar(f"neq_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] != self._previous_solution[position]).OnlyEnforceIf(b)
                self._model.Add(self._grid_vars[position] == self._previous_solution[position]).OnlyEnforceIf(b.Not())
                negated_constraints_bools.append(b)

        if not negated_constraints_bools:
            return Grid.empty()

        self._model.AddBoolOr(negated_constraints_bools)
        return self.get_solution()

    def _add_constraints(self):
        self._add_input_constraints()
        self._add_neighbors_constraints()
        self._add_flow_constraints()
        self._add_count_constraints()

    def _add_input_constraints(self):
        for position, val in self._grid:
            if val == self.Empty:
                self._add_input_empty_constraint(position)
                continue

            if val == self.Black:
                self._add_input_black_constraint(position)
                continue

            self._add_number_input_constraint(position)

    def _add_input_empty_constraint(self, position: Position):
        self._model.Add(self._grid_vars[position] >= 1)
        self._model.Add(self._rank_vars[position] > 0)

    def _add_input_black_constraint(self, position: Position):
        self._model.Add(self._grid_vars[position] == 0)
        self._model.Add(self._rank_vars[position] == 0)
        self._model.Add(self._region_id_vars[position] == -1)

    def _add_number_input_constraint(self, position: Position):
        self._model.Add(self._grid_vars[position] == 0)
        self._model.Add(self._rank_vars[position] == 0)
        self._model.Add(self._region_id_vars[position] == self._region_id_by_position[position])

    def _add_neighbors_constraints(self):
        for position in [position for position, value in self._grid if value == self.Empty]:
            if (position_right := position.right) in self._grid:
                self._model.Add(self._grid_vars[position] != self._grid_vars[position_right])
            if (position_down := position.down) in self._grid:
                self._model.Add(self._grid_vars[position] != self._grid_vars[position_down])

    def _add_flow_constraints(self):
        value_by_direction = {
            Direction.up(): self.up,
            Direction.down(): self.down,
            Direction.right(): self.right,
            Direction.left(): self.left
        }

        for position, _ in self._grid:
            for neighbor_pos in position.neighbors():
                direction = position.direction_to(neighbor_pos)
                value = value_by_direction[direction]
                if neighbor_pos not in self._grid:
                    self._model.Add(self._grid_vars[position] != value)
                    continue

                points_direction = self._model.NewBoolVar(f"points_{direction}_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] == value).OnlyEnforceIf(points_direction)
                self._model.Add(self._grid_vars[position] != value).OnlyEnforceIf(points_direction.Not())

                self._model.Add(self._region_id_vars[position] == self._region_id_vars[neighbor_pos]).OnlyEnforceIf(points_direction)
                self._model.Add(self._rank_vars[position] == self._rank_vars[neighbor_pos] + 1).OnlyEnforceIf(points_direction)

    def _add_count_constraints(self):
        for region_id, val in self.value_by_region_id.items():
            region_indicators = []
            for current_position, region_id_var in self._region_id_vars:
                indicator = self._model.NewBoolVar(f"in_region_{region_id}_{current_position}")
                self._model.Add(region_id_var == region_id).OnlyEnforceIf(indicator)
                self._model.Add(region_id_var != region_id).OnlyEnforceIf(indicator.Not())
                region_indicators.append(indicator)
            self._model.Add(sum(region_indicators) == val + 1)
