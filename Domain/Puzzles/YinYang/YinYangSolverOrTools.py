from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class YinYangSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 6:
            raise ValueError("Yin Yang grid must be at least 6x6")

        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._solver.parameters.max_time_in_seconds = 120.0  # Fail fast if stuck
        self._grid_vars = {}
        self._previous_solution = None

        self._init_model()

    def _init_model(self):
        # 1. Grid Variables
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._grid_vars[(r, c)] = self._model.NewBoolVar(f"cell_{r}_{c}")

        # 2. Base Rules (Fixed values, 2x2, Checkerboard)
        self._add_base_constraints()

        # 3. Connectivity Rules (Rank/Flow based)
        self._add_connectivity_constraints()

    def _add_base_constraints(self):
        # Initial values
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                val = self._grid[Position(r, c)]
                if val == 1:  # White
                    self._model.Add(self._grid_vars[(r, c)] == 1)
                elif val == 0:  # Black
                    self._model.Add(self._grid_vars[(r, c)] == 0)

        # 2x2 Constraints (No solid square)
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                cells = [
                    self._grid_vars[(r, c)],
                    self._grid_vars[(r + 1, c)],
                    self._grid_vars[(r, c + 1)],
                    self._grid_vars[(r + 1, c + 1)],
                ]
                self._model.Add(sum(cells) > 0)
                self._model.Add(sum(cells) < 4)

        # Checkerboard Constraints
        # Forbidden: 1 0 / 0 1 and 0 1 / 1 0
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                self._model.AddForbiddenAssignments(
                    [
                        self._grid_vars[(r, c)],
                        self._grid_vars[(r, c + 1)],
                        self._grid_vars[(r + 1, c)],
                        self._grid_vars[(r + 1, c + 1)],
                    ],
                    [(1, 0, 0, 1), (0, 1, 1, 0)],
                )

    def _add_connectivity_constraints(self):
        # Rank variables: 0 to N*M - 1
        num_cells = self.rows_number * self.columns_number
        rank_vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                rank_vars[(r, c)] = self._model.NewIntVar(0, num_cells - 1, f"rank_{r}_{c}")

        # Root indicators
        root_white = {}
        root_black = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                root_white[(r, c)] = self._model.NewBoolVar(f"root_white_{r}_{c}")
                root_black[(r, c)] = self._model.NewBoolVar(f"root_black_{r}_{c}")

        # Exactly one root per color
        self._model.Add(sum(root_white.values()) == 1)
        self._model.Add(sum(root_black.values()) == 1)

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                u_pos = (r, c)
                u_grid = self._grid_vars[u_pos]
                u_rank = rank_vars[u_pos]
                u_rw = root_white[u_pos]
                u_rb = root_black[u_pos]

                # Root implications
                self._model.Add(u_grid == 1).OnlyEnforceIf(u_rw)
                self._model.Add(u_rank == 0).OnlyEnforceIf(u_rw)

                self._model.Add(u_grid == 0).OnlyEnforceIf(u_rb)
                self._model.Add(u_rank == 0).OnlyEnforceIf(u_rb)

                # Neighbors
                neighbors = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows_number and 0 <= nc < self.columns_number:
                        neighbors.append((nr, nc))

                # Connectivity logic
                parents_white = []
                parents_black = []

                for v_pos in neighbors:
                    # Parent White: v is parent of u (white)
                    # Means: grid[u]==1, grid[v]==1, rank[v] == rank[u] - 1
                    pw = self._model.NewBoolVar(f"pw_{u_pos}_{v_pos}")
                    v_grid = self._grid_vars[v_pos]
                    v_rank = rank_vars[v_pos]

                    self._model.Add(u_grid == 1).OnlyEnforceIf(pw)
                    self._model.Add(v_grid == 1).OnlyEnforceIf(pw)
                    self._model.Add(v_rank == u_rank - 1).OnlyEnforceIf(pw)
                    parents_white.append(pw)

                    # Parent Black: v is parent of u (black)
                    # Means: grid[u]==0, grid[v]==0, rank[v] == rank[u] - 1
                    pb = self._model.NewBoolVar(f"pb_{u_pos}_{v_pos}")
                    self._model.Add(u_grid == 0).OnlyEnforceIf(pb)
                    self._model.Add(v_grid == 0).OnlyEnforceIf(pb)
                    self._model.Add(v_rank == u_rank - 1).OnlyEnforceIf(pb)
                    parents_black.append(pb)

                # If u is White, (u is root) OR (exists white parent)
                self._model.AddBoolOr([u_rw] + parents_white).OnlyEnforceIf(u_grid)

                # If u is Black, (u is root) OR (exists black parent)
                self._model.AddBoolOr([u_rb] + parents_black).OnlyEnforceIf(u_grid.Not())

    def get_solution(self) -> Grid:
        status = self._solver.Solve(self._model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution_grid = self._build_grid_from_solution()
            self._previous_solution = solution_grid
            return solution_grid
        else:
            return Grid.empty()

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        # Exclude previous solution
        constraints = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                val = self._previous_solution[Position(r, c)]
                if val == 1:
                    constraints.append(self._grid_vars[(r, c)].Not())
                else:
                    constraints.append(self._grid_vars[(r, c)])

        self._model.AddBoolOr(constraints)

        return self.get_solution()

    def _build_grid_from_solution(self) -> Grid:
        data = []
        for r in range(self.rows_number):
            row_data = []
            for c in range(self.columns_number):
                val = self._solver.Value(self._grid_vars[(r, c)])
                row_data.append(int(val))
            data.append(row_data)
        return Grid(data)
