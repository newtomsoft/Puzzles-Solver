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
        self._solver.parameters.max_time_in_seconds = 120.0
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

        # 4. Boundary Loop Constraints (Degree optimization)
        self._add_boundary_constraints()

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
        num_cells = self.rows_number * self.columns_number
        rank_vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                rank_vars[(r, c)] = self._model.NewIntVar(0, num_cells - 1, f"rank_{r}_{c}")

        root_white = {}
        root_black = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                root_white[(r, c)] = self._model.NewBoolVar(f"root_white_{r}_{c}")
                root_black[(r, c)] = self._model.NewBoolVar(f"root_black_{r}_{c}")

        self._model.Add(sum(root_white.values()) == 1)
        self._model.Add(sum(root_black.values()) == 1)

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                u_pos = (r, c)
                u_grid = self._grid_vars[u_pos]
                u_rank = rank_vars[u_pos]
                u_rw = root_white[u_pos]
                u_rb = root_black[u_pos]

                self._model.Add(u_grid == 1).OnlyEnforceIf(u_rw)
                self._model.Add(u_rank == 0).OnlyEnforceIf(u_rw)

                self._model.Add(u_grid == 0).OnlyEnforceIf(u_rb)
                self._model.Add(u_rank == 0).OnlyEnforceIf(u_rb)

                neighbors = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows_number and 0 <= nc < self.columns_number:
                        neighbors.append((nr, nc))

                parents_white = []
                parents_black = []

                for v_pos in neighbors:
                    pw = self._model.NewBoolVar(f"pw_{u_pos}_{v_pos}")
                    v_grid = self._grid_vars[v_pos]
                    v_rank = rank_vars[v_pos]

                    self._model.Add(u_grid == 1).OnlyEnforceIf(pw)
                    self._model.Add(v_grid == 1).OnlyEnforceIf(pw)
                    self._model.Add(v_rank == u_rank - 1).OnlyEnforceIf(pw)
                    parents_white.append(pw)

                    pb = self._model.NewBoolVar(f"pb_{u_pos}_{v_pos}")
                    self._model.Add(u_grid == 0).OnlyEnforceIf(pb)
                    self._model.Add(v_grid == 0).OnlyEnforceIf(pb)
                    self._model.Add(v_rank == u_rank - 1).OnlyEnforceIf(pb)
                    parents_black.append(pb)

                self._model.AddBoolOr([u_rw] + parents_white).OnlyEnforceIf(u_grid)
                self._model.AddBoolOr([u_rb] + parents_black).OnlyEnforceIf(u_grid.Not())

    def _add_boundary_constraints(self):
        # Horizontal edges: (r, c) to (r+1, c).
        # Note: In previous plan I defined h_edge as (r,c) to (r,c+1). Standard terminology:
        # H-Edge is horizontal line? Or separates vertically?
        # Let's stick to variable names:
        # h_edge[r][c] separates grid[r][c] and grid[r+1][c]. (Horizontal divider).
        # v_edge[r][c] separates grid[r][c] and grid[r][c+1]. (Vertical divider).

        h_edges = {}
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number):
                edge = self._model.NewBoolVar(f"h_edge_{r}_{c}")
                u = self._grid_vars[(r, c)]
                v = self._grid_vars[(r + 1, c)]
                # edge = u XOR v
                self._model.AddAllowedAssignments([u, v, edge], [(0,0,0), (0,1,1), (1,0,1), (1,1,0)])
                h_edges[(r, c)] = edge

        v_edges = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number - 1):
                edge = self._model.NewBoolVar(f"v_edge_{r}_{c}")
                u = self._grid_vars[(r, c)]
                v = self._grid_vars[(r, c + 1)]
                self._model.AddAllowedAssignments([u, v, edge], [(0,0,0), (0,1,1), (1,0,1), (1,1,0)])
                v_edges[(r, c)] = edge

        # Corner Degree Constraints
        # Corner at (r, c) intersection means intersection of row-line r and col-line c.
        # It involves:
        # h_edges[(r-1, c-1)] (Left part of row-line r) -- Wait.
        # Row-line r is between row r-1 and r? No, indices 0..R-1.
        # h_edge[r] is between grid[r] and grid[r+1].
        # So row-line 'r' corresponds to `h_edge[r]`.
        # h_edge[r][c] is segment at column c.

        # Corner indices: r from 0 to Rows-2 (edges). Corner is intersection of h_edge[r] and v_edge[c].
        # Actually, Corner (r, c) is intersection of:
        # h_edge[r][c] (Right of corner)
        # h_edge[r][c-1] (Left of corner) -- Assuming we iterate corners
        # v_edge[r][c] (Bottom of corner)
        # v_edge[r+1][c] (Top of corner)? No.

        # Let's visualize grid indices.
        # Cells (r,c).
        # h_edge[r][c] is below cell (r,c).
        # v_edge[r][c] is right of cell (r,c).
        # Corner (r, c) is bottom-right of cell (r,c).
        # Edges meeting at Corner (r, c):
        # 1. Top: v_edge[r][c] (Right of (r,c)) - No, that's right of cell.
        #    v_edge[r][c] goes from Corner(r-1, c) to Corner(r, c). (Right side of cell r,c).
        #    So it's the Top edge coming into corner.
        # 2. Bottom: v_edge[r+1][c] (Right of cell (r+1, c)).
        #    It goes from Corner(r, c) to Corner(r+1, c).
        # 3. Left: h_edge[r][c] (Bottom of cell (r,c)).
        #    Goes from Corner(r, c-1) to Corner(r, c).
        # 4. Right: h_edge[r][c+1] (Bottom of cell (r,c+1)).
        #    Goes from Corner(r, c) to Corner(r, c+1).

        # Checking indices limits.
        # We iterate corners strictly inside the grid.
        # Inner corners correspond to:
        # r in 0 .. Rows-2. (Separating row r and r+1).
        # c in 0 .. Cols-2. (Separating col c and c+1).
        # The corner is the cross point.

        # Edges incident to this cross point:
        # h_edge[r][c] (Left part, below (r,c))
        # h_edge[r][c+1] (Right part, below (r, c+1))
        # v_edge[r][c] (Top part, right of (r, c))
        # v_edge[r+1][c] (Bottom part, right of (r+1, c))

        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                incident = [
                    h_edges[(r, c)],
                    h_edges[(r, c+1)],
                    v_edges[(r, c)],
                    v_edges[(r+1, c)]
                ]
                # Degree must be 0 or 2.
                # 4 is already forbidden by checkerboard (implicit), but we can explicit.
                self._model.Add(sum(incident) != 1)
                self._model.Add(sum(incident) != 3)

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
