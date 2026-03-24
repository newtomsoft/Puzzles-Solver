from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class FillominoSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.grid = grid
        self.rows = self.grid.rows_number
        self.cols = self.grid.columns_number
        self.max_val = self.rows * self.cols
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.cell_vars = Grid.empty()
        self._init_solver()
        self._previous_solution = Grid.empty()

    def _init_solver(self):
        self.cell_vars = Grid([[self.model.new_int_var(1, self.max_val, f"cell_{r}_{c}") for c in range(self.cols)] for r in range(self.rows)])

        for cell_var_pos, val in [(self.cell_vars[pos], val) for pos, val in self.grid if isinstance(val, int) and val > 0]:
            self.model.add(cell_var_pos == val)

    def get_solution(self) -> Grid:
        iteration = 0
        while self.solver.solve(self.model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            iteration += 1
            current_solution = Grid([[self.solver.value(self.cell_vars[(r, c)]) for c in range(self.cols)] for r in range(self.rows)])
            if self._validate_and_add_constraints(current_solution, iteration):
                self._previous_solution = current_solution
                return current_solution

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution.is_empty():
            return Grid.empty()

        literals = []
        for r in range(self.rows):
            for c in range(self.cols):
                val = self._previous_solution[r][c]
                # Create a boolean variable that is true if the cell is different from previous value
                is_diff = self.model.new_bool_var(f'diff_{r}_{c}_sol')
                self.model.add(self.cell_vars[(r, c)] != val).only_enforce_if(is_diff)
                self.model.add(self.cell_vars[(r, c)] == val).only_enforce_if(is_diff.negated())
                literals.append(is_diff)

        self.model.add_bool_or(literals)

        return self.get_solution()

    def _validate_and_add_constraints(self, current_solution: Grid, iteration: int):
        visited = set()
        all_valid = True
        cuts_added = 0

        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in visited:
                    continue

                value = current_solution[r][c]
                component = []
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

                size = len(component)

                if size != value:
                    all_valid = False
                    cuts_added += 1

                    if size < value:
                        literals = []
                        for cr, cc in component:
                            is_val = self.model.new_bool_var(f'is_{cr}_{cc}_{value}_iter{iteration}_{cuts_added}')
                            self.model.add(self.cell_vars[(cr, cc)] == value).only_enforce_if(is_val)
                            self.model.add(self.cell_vars[(cr, cc)] != value).only_enforce_if(is_val.negated())
                            # We want NOT is_val to be in the OR clause
                            literals.append(is_val.negated())

                        potential_neighbors = set()
                        for cr, cc in component:
                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                nr, nc = cr + dr, cc + dc
                                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                    if (nr, nc) not in component:
                                        potential_neighbors.add((nr, nc))

                        for nr, nc in potential_neighbors:
                            is_neighbor_val = self.model.new_bool_var(f'is_n_{nr}_{nc}_{value}_iter{iteration}_{cuts_added}')
                            self.model.add(self.cell_vars[(nr, nc)] == value).only_enforce_if(is_neighbor_val)
                            self.model.add(self.cell_vars[(nr, nc)] != value).only_enforce_if(is_neighbor_val.negated())
                            literals.append(is_neighbor_val)

                        self.model.add_bool_or(literals)

                    else:  # size > value
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
                                b_u = self.model.new_bool_var(f'is_{ur}_{uc}_{value}_iter{iteration}_{cuts_added}')
                                self.model.add(self.cell_vars[(ur, uc)] == value).only_enforce_if(b_u)
                                self.model.add(self.cell_vars[(ur, uc)] != value).only_enforce_if(b_u.negated())
                                cell_is_val_vars[u] = b_u

                            if v not in cell_is_val_vars:
                                b_v = self.model.new_bool_var(f'is_{vr}_{vc}_{value}_iter{iteration}_{cuts_added}')
                                self.model.add(self.cell_vars[(vr, vc)] == value).only_enforce_if(b_v)
                                self.model.add(self.cell_vars[(vr, vc)] != value).only_enforce_if(b_v.negated())
                                cell_is_val_vars[v] = b_v

                            b_u = cell_is_val_vars[u]
                            b_v = cell_is_val_vars[v]

                            b_edge = self.model.new_bool_var(f'edge_{ur}_{uc}_{vr}_{vc}_iter{iteration}_{cuts_added}')
                            self.model.add_bool_and([b_u, b_v]).only_enforce_if(b_edge)
                            self.model.add_bool_or([b_u.negated(), b_v.negated()]).only_enforce_if(b_edge.negated())
                            edge_bools.append(b_edge)

                        if internal_edges:
                            self.model.add(sum(edge_bools) <= len(internal_edges) - 1)

        return all_valid
