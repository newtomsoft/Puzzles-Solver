from ortools.sat.python import cp_model
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class FobidoshiSolver(GameSolver):
    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_ortools = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_ortools = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                self._grid_ortools[(r, c)] = self._model.new_bool_var(f"cell_{r}_{c}")
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_ortools is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution_values = []
            for r in range(self._rows_number):
                row = []
                for c in range(self._columns_number):
                    row.append(1 if self._solver.boolean_value(self._grid_ortools[(r, c)]) else 0)
                solution_values.append(row)
            solution = Grid(solution_values)
            self._previous_solution = solution
            return solution

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return Grid.empty()

        match_vars = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                if self._previous_solution.value(r, c) == 1:
                    match_vars.append(self._grid_ortools[(r, c)])
                else:
                    match_vars.append(self._grid_ortools[(r, c)].negated())

        self._model.add_bool_or([var.negated() for var in match_vars])

        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_not_same_4_adjacent_constraints()
        self._add_connectivity_constraints()

    def _add_connectivity_constraints(self):
        root = None
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                if self._grid.value(r, c) == 1:
                    root = (r, c)
                    break
            if root:
                break

        if root is None:
            return

        dist = {}
        max_dist = self._rows_number * self._columns_number
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                dist[(r, c)] = self._model.new_int_var(0, max_dist, f"dist_{r}_{c}")

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                is_circle = self._grid_ortools[(r, c)]
                d = dist[(r, c)]

                if (r, c) == root:
                    self._model.add(is_circle == 1)
                    self._model.add(d == 0)
                else:
                    neighbors = self._get_neighbors(r, c)
                    
                    self._model.add(d > 0).only_enforce_if(is_circle)
                    
                    possible_parents = []
                    for nr, nc in neighbors:
                        p_ok = self._model.new_bool_var(f"pok_{r}_{c}_{nr}_{nc}")
                        self._model.add(self._grid_ortools[(nr, nc)] == 1).only_enforce_if(p_ok)
                        self._model.add(d == dist[(nr, nc)] + 1).only_enforce_if(p_ok)
                        possible_parents.append(p_ok)
                    
                    self._model.add_bool_or(possible_parents).only_enforce_if(is_circle)

                self._model.add(d == 0).only_enforce_if(is_circle.negated())

    def _get_neighbors(self, r, c):
        neighbors = []
        if r > 0: neighbors.append((r - 1, c))
        if r < self._rows_number - 1: neighbors.append((r + 1, c))
        if c > 0: neighbors.append((r, c - 1))
        if c < self._columns_number - 1: neighbors.append((r, c + 1))
        return neighbors

    def _add_initial_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._grid.value(r, c)
                if val == 1:
                    self._model.add(self._grid_ortools[(r, c)] == 1)
                elif val == 0:
                    self._model.add(self._grid_ortools[(r, c)] == 0)

    def _add_not_same_4_adjacent_constraints(self):
        # 4 cercles consécutifs interdits (Max 3 cercles)
        # Mais 4 cases vides (0) sont autorisées
        for r in range(self._rows_number):
            for c in range(self._columns_number - 3):
                cells = [self._grid_ortools[(r, c + i)] for i in range(4)]
                self._model.add_bool_or([cell.negated() for cell in cells])

        for c in range(self._columns_number):
            for r in range(self._rows_number - 3):
                cells = [self._grid_ortools[(r + i, c)] for i in range(4)]
                self._model.add_bool_or([cell.negated() for cell in cells])
