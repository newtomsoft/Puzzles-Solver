from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid

class FillominoSolver:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.rows = self.grid.rows_number
        self.cols = self.grid.columns_number
        self.max_val = self.rows * self.cols
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.cell_vars = {}
        self._init_solver()

    def _init_solver(self):
        # Create variables
        for r in range(self.rows):
            for c in range(self.cols):
                self.cell_vars[(r, c)] = self.model.NewIntVar(1, self.max_val, f'cell_{r}_{c}')

        # Initial constraints from grid
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.grid[r][c]
                if isinstance(val, int) and val > 0:
                    self.model.Add(self.cell_vars[(r, c)] == val)

    def solve(self):
        iteration = 0
        while True:
            iteration += 1
            status = self.solver.Solve(self.model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return Grid.empty()

            # internal solution grid (integers)
            current_solution = [[self.solver.Value(self.cell_vars[(r, c)])
                                 for c in range(self.cols)]
                                for r in range(self.rows)]

            # Check connectivity and size constraints
            if self._validate_and_add_constraints(current_solution, iteration):
                return Grid(current_solution)

    def _validate_and_add_constraints(self, current_solution, iteration):
        visited = set()
        all_valid = True
        cuts_added = 0

        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in visited:
                    continue

                # BFS to find connected component of same value
                value = current_solution[r][c]
                component = []
                queue = [(r, c)]
                visited.add((r, c))
                component.append((r, c))

                idx = 0
                while idx < len(component):
                    curr_r, curr_c = component[idx]
                    idx += 1

                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if (nr, nc) not in visited and current_solution[nr][nc] == value:
                                visited.add((nr, nc))
                                component.append((nr, nc))
                                queue.append((nr, nc))

                size = len(component)

                if size != value:
                    all_valid = False
                    cuts_added += 1

                    if size < value:
                        # Region is too small, must expand.
                        # Constraint: (All cells in C are V) => (At least one neighbor is V)
                        # Equivalent to: OR( cell != V for cell in C ) OR OR( neighbor == V for neighbor in Neighbors )

                        literals = []

                        # Part 1: If any cell in Component is NOT V, the condition is satisfied (we abandoned this region hypothesis)
                        for cr, cc in component:
                            # We need a bool for x[c] != V
                            # Alternatively, use x[c] == V implies Neighbor=V

                            is_val = self.model.NewBoolVar(f'is_{cr}_{cc}_{value}_iter{iteration}_{cuts_added}')
                            self.model.Add(self.cell_vars[(cr, cc)] == value).OnlyEnforceIf(is_val)
                            self.model.Add(self.cell_vars[(cr, cc)] != value).OnlyEnforceIf(is_val.Not())
                            # We want NOT is_val to be in the OR clause
                            literals.append(is_val.Not())

                        # Part 2: Neighbors
                        potential_neighbors = set()
                        for cr, cc in component:
                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                nr, nc = cr + dr, cc + dc
                                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                    if (nr, nc) not in component:
                                        potential_neighbors.add((nr, nc))

                        for nr, nc in potential_neighbors:
                            is_neighbor_val = self.model.NewBoolVar(f'is_n_{nr}_{nc}_{value}_iter{iteration}_{cuts_added}')
                            self.model.Add(self.cell_vars[(nr, nc)] == value).OnlyEnforceIf(is_neighbor_val)
                            self.model.Add(self.cell_vars[(nr, nc)] != value).OnlyEnforceIf(is_neighbor_val.Not())
                            literals.append(is_neighbor_val)

                        self.model.AddBoolOr(literals)

                    else: # size > value
                        # Region is too big. Break connectivity.
                        internal_edges = []
                        comp_set = set(component)
                        for cr, cc in component:
                            for dr, dc in [(1, 0), (0, 1)]:
                                nr, nc = cr + dr, cc + dc
                                if (nr, nc) in comp_set:
                                    internal_edges.append(((cr, cc), (nr, nc)))

                        edge_bools = []
                        cell_is_val_vars = {}

                        for (u, v) in internal_edges:
                            ur, uc = u
                            vr, vc = v

                            if u not in cell_is_val_vars:
                                b_u = self.model.NewBoolVar(f'is_{ur}_{uc}_{value}_iter{iteration}_{cuts_added}')
                                self.model.Add(self.cell_vars[(ur, uc)] == value).OnlyEnforceIf(b_u)
                                self.model.Add(self.cell_vars[(ur, uc)] != value).OnlyEnforceIf(b_u.Not())
                                cell_is_val_vars[u] = b_u

                            if v not in cell_is_val_vars:
                                b_v = self.model.NewBoolVar(f'is_{vr}_{vc}_{value}_iter{iteration}_{cuts_added}')
                                self.model.Add(self.cell_vars[(vr, vc)] == value).OnlyEnforceIf(b_v)
                                self.model.Add(self.cell_vars[(vr, vc)] != value).OnlyEnforceIf(b_v.Not())
                                cell_is_val_vars[v] = b_v

                            b_u = cell_is_val_vars[u]
                            b_v = cell_is_val_vars[v]

                            b_edge = self.model.NewBoolVar(f'edge_{ur}_{uc}_{vr}_{vc}_iter{iteration}_{cuts_added}')
                            self.model.AddBoolAnd([b_u, b_v]).OnlyEnforceIf(b_edge)
                            self.model.AddBoolOr([b_u.Not(), b_v.Not()]).OnlyEnforceIf(b_edge.Not())
                            edge_bools.append(b_edge)

                        if internal_edges:
                            self.model.Add(sum(edge_bools) <= len(internal_edges) - 1)

        return all_valid
