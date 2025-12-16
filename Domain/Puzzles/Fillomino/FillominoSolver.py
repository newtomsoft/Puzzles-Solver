from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid


class FillominoSolver:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.rows = self.grid.rows_number
        self.cols = self.grid.columns_number
        self.model = cp_model.CpModel()

        self.max_cell_var = max([value for _, value in self.grid])
        self.max_region_size = self.rows * self.cols

        self.cell_vars = {}
        self.region_id_vars = {}
        self.is_root = {}
        self.depth = {}
        self.parent_choice = {}

    def solve(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.cell_vars[(r, c)] = self.model.NewIntVar(1, self.max_cell_var, f'cell_{r}_{c}')
                self.region_id_vars[(r, c)] = self.model.NewIntVar(0, self.rows * self.cols - 1, f'region_{r}_{c}')
                self.is_root[(r, c)] = self.model.NewBoolVar(f'is_root_{r}_{c}')
                self.depth[(r, c)] = self.model.NewIntVar(0, self.max_region_size - 1, f'depth_{r}_{c}')
                self.parent_choice[(r, c)] = self.model.NewIntVar(0, 4, f'parent_choice_{r}_{c}')

        self._add_initial_constraints()
        self._add_adjacency_constraints()
        self._add_region_size_and_linking_constraints()
        self._add_connectivity_constraints()

        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return Grid([[solver.Value(self.cell_vars[(r, c)]) for c in range(self.cols)] for r in range(self.rows)])
        else:
            return Grid.empty()

    def _add_initial_constraints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if isinstance(self.grid[r][c], int) and self.grid[r][c] > 0:
                    self.model.Add(self.cell_vars[(r, c)] == self.grid[r][c])

    def _add_connectivity_constraints(self):
        for r_idx in range(self.rows):
            for c_idx in range(self.cols):
                current_cell_id = r_idx * self.cols + c_idx

                self.model.Add(self.depth[(r_idx, c_idx)] == 0).OnlyEnforceIf(self.is_root[(r_idx, c_idx)])
                self.model.Add(self.parent_choice[(r_idx, c_idx)] == 4).OnlyEnforceIf(self.is_root[(r_idx, c_idx)])
                self.model.Add(self.region_id_vars[(r_idx, c_idx)] == current_cell_id).OnlyEnforceIf(self.is_root[(r_idx, c_idx)])

                self.model.Add(self.parent_choice[(r_idx, c_idx)] < 4).OnlyEnforceIf(self.is_root[(r_idx, c_idx)].Not())
                self.model.Add(self.depth[(r_idx, c_idx)] > 0).OnlyEnforceIf(self.is_root[(r_idx, c_idx)].Not())

                cond_parent_up = self.model.NewBoolVar(f'p_up_{r_idx}{c_idx}')
                self.model.Add(self.parent_choice[(r_idx, c_idx)] == 0).OnlyEnforceIf(cond_parent_up)
                self.model.Add(self.parent_choice[(r_idx, c_idx)] != 0).OnlyEnforceIf(cond_parent_up.Not())
                self.model.AddImplication(cond_parent_up, self.is_root[(r_idx, c_idx)].Not())
                if r_idx > 0:
                    self.model.Add(self.region_id_vars[(r_idx, c_idx)] == self.region_id_vars[(r_idx - 1, c_idx)]).OnlyEnforceIf(cond_parent_up)
                    self.model.Add(self.depth[(r_idx, c_idx)] == self.depth[(r_idx - 1, c_idx)] + 1).OnlyEnforceIf(cond_parent_up)
                    self.model.Add(self.depth[(r_idx, c_idx)] < self.cell_vars[(r_idx, c_idx)]).OnlyEnforceIf(cond_parent_up)
                else:
                    self.model.Add(cond_parent_up == 0)

                cond_parent_right = self.model.NewBoolVar(f'p_right_{r_idx}{c_idx}')
                self.model.Add(self.parent_choice[(r_idx, c_idx)] == 1).OnlyEnforceIf(cond_parent_right)
                self.model.Add(self.parent_choice[(r_idx, c_idx)] != 1).OnlyEnforceIf(cond_parent_right.Not())
                self.model.AddImplication(cond_parent_right, self.is_root[(r_idx, c_idx)].Not())
                if c_idx < self.cols - 1:
                    self.model.Add(self.region_id_vars[(r_idx, c_idx)] == self.region_id_vars[(r_idx, c_idx + 1)]).OnlyEnforceIf(cond_parent_right)
                    self.model.Add(self.depth[(r_idx, c_idx)] == self.depth[(r_idx, c_idx + 1)] + 1).OnlyEnforceIf(cond_parent_right)
                    self.model.Add(self.depth[(r_idx, c_idx)] < self.cell_vars[(r_idx, c_idx)]).OnlyEnforceIf(cond_parent_right)
                else:
                    self.model.Add(cond_parent_right == 0)

                cond_parent_down = self.model.NewBoolVar(f'p_down_{r_idx}{c_idx}')
                self.model.Add(self.parent_choice[(r_idx, c_idx)] == 2).OnlyEnforceIf(cond_parent_down)
                self.model.Add(self.parent_choice[(r_idx, c_idx)] != 2).OnlyEnforceIf(cond_parent_down.Not())
                self.model.AddImplication(cond_parent_down, self.is_root[(r_idx, c_idx)].Not())
                if r_idx < self.rows - 1:
                    self.model.Add(self.region_id_vars[(r_idx, c_idx)] == self.region_id_vars[(r_idx + 1, c_idx)]).OnlyEnforceIf(cond_parent_down)
                    self.model.Add(self.depth[(r_idx, c_idx)] == self.depth[(r_idx + 1, c_idx)] + 1).OnlyEnforceIf(cond_parent_down)
                    self.model.Add(self.depth[(r_idx, c_idx)] < self.cell_vars[(r_idx, c_idx)]).OnlyEnforceIf(cond_parent_down)
                else:
                    self.model.Add(cond_parent_down == 0)

                cond_parent_left = self.model.NewBoolVar(f'p_left_{r_idx}{c_idx}')
                self.model.Add(self.parent_choice[(r_idx, c_idx)] == 3).OnlyEnforceIf(cond_parent_left)
                self.model.Add(self.parent_choice[(r_idx, c_idx)] != 3).OnlyEnforceIf(cond_parent_left.Not())
                self.model.AddImplication(cond_parent_left, self.is_root[(r_idx, c_idx)].Not())
                if c_idx > 0:
                    self.model.Add(self.region_id_vars[(r_idx, c_idx)] == self.region_id_vars[(r_idx, c_idx - 1)]).OnlyEnforceIf(cond_parent_left)
                    self.model.Add(self.depth[(r_idx, c_idx)] == self.depth[(r_idx, c_idx - 1)] + 1).OnlyEnforceIf(cond_parent_left)
                    self.model.Add(self.depth[(r_idx, c_idx)] < self.cell_vars[(r_idx, c_idx)]).OnlyEnforceIf(cond_parent_left)
                else:
                    self.model.Add(cond_parent_left == 0)
        for pr_root_check in range(self.rows):
            for pc_root_check in range(self.cols):
                k_root_idx_check = pr_root_check * self.cols + pc_root_check

                is_k_root_id_used_by_any_cell = self.model.NewBoolVar(f'k_used_{k_root_idx_check}')
                reified_literals_for_k_used = []
                for r_cell_idx in range(self.rows):
                    for c_cell_idx in range(self.cols):
                        b_cell_uses_k = self.model.NewBoolVar(f'b_cell_{r_cell_idx}{c_cell_idx}_uses_k_{k_root_idx_check}')
                        self.model.Add(self.region_id_vars[(r_cell_idx, c_cell_idx)] == k_root_idx_check).OnlyEnforceIf(b_cell_uses_k)
                        self.model.Add(self.region_id_vars[(r_cell_idx, c_cell_idx)] != k_root_idx_check).OnlyEnforceIf(b_cell_uses_k.Not())
                        reified_literals_for_k_used.append(b_cell_uses_k)

                self.model.AddBoolOr(reified_literals_for_k_used).OnlyEnforceIf(is_k_root_id_used_by_any_cell)
                all_reified_false = [b.Not() for b in reified_literals_for_k_used]
                self.model.AddBoolAnd(all_reified_false).OnlyEnforceIf(is_k_root_id_used_by_any_cell.Not())

                self.model.AddImplication(is_k_root_id_used_by_any_cell, self.is_root[(pr_root_check, pc_root_check)])

    def _add_region_size_and_linking_constraints(self):
        self.actual_region_sizes = [self.model.NewIntVar(0, self.max_region_size, f'ars_{k}') for k in range(self.rows * self.cols)]
        for k_root_idx in range(self.rows * self.cols):
            pr = k_root_idx // self.cols
            pc = k_root_idx % self.cols

            is_cell_member_of_k_bools = []
            for r_cell in range(self.rows):
                for c_cell in range(self.cols):
                    b_is_member = self.model.NewBoolVar(f'is_cell_{r_cell}{c_cell}_in_region_{pr}{pc}')
                    self.model.Add(self.region_id_vars[(r_cell, c_cell)] == k_root_idx).OnlyEnforceIf(b_is_member)
                    self.model.Add(self.region_id_vars[(r_cell, c_cell)] != k_root_idx).OnlyEnforceIf(b_is_member.Not())
                    is_cell_member_of_k_bools.append(b_is_member)

            current_sum_of_members = self.model.NewIntVar(0, self.max_region_size, f'sum_members_{pr}{pc}')
            self.model.Add(current_sum_of_members == sum(is_cell_member_of_k_bools))

            self.model.Add(self.actual_region_sizes[k_root_idx] == current_sum_of_members).OnlyEnforceIf(self.is_root[(pr, pc)])
            self.model.Add(self.actual_region_sizes[k_root_idx] == 0).OnlyEnforceIf(self.is_root[(pr, pc)].Not())
        for r in range(self.rows):
            for c in range(self.cols):
                self.model.AddElement(self.region_id_vars[(r, c)], self.actual_region_sizes, self.cell_vars[(r, c)])

    def _add_adjacency_constraints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if c + 1 < self.cols:
                    r1, c1, r2, c2 = r, c, r, c + 1
                    b_region_eq_h = self.model.NewBoolVar(f'b_region_eq_h_{r1}{c1}')
                    self.model.Add(self.region_id_vars[(r1, c1)] == self.region_id_vars[(r2, c2)]).OnlyEnforceIf(b_region_eq_h)
                    self.model.Add(self.region_id_vars[(r1, c1)] != self.region_id_vars[(r2, c2)]).OnlyEnforceIf(b_region_eq_h.Not())

                    b_cell_eq_h = self.model.NewBoolVar(f'b_cell_eq_h_{r1}{c1}')
                    self.model.Add(self.cell_vars[(r1, c1)] == self.cell_vars[(r2, c2)]).OnlyEnforceIf(b_cell_eq_h)
                    self.model.Add(self.cell_vars[(r1, c1)] != self.cell_vars[(r2, c2)]).OnlyEnforceIf(b_cell_eq_h.Not())

                    self.model.AddImplication(b_region_eq_h, b_cell_eq_h)
                    self.model.AddImplication(b_cell_eq_h, b_region_eq_h)
                if r + 1 < self.rows:
                    r1, c1, r2, c2 = r, c, r + 1, c
                    b_region_eq_v = self.model.NewBoolVar(f'b_region_eq_v_{r1}{c1}')
                    self.model.Add(self.region_id_vars[(r1, c1)] == self.region_id_vars[(r2, c2)]).OnlyEnforceIf(b_region_eq_v)
                    self.model.Add(self.region_id_vars[(r1, c1)] != self.region_id_vars[(r2, c2)]).OnlyEnforceIf(b_region_eq_v.Not())

                    b_cell_eq_v = self.model.NewBoolVar(f'b_cell_eq_v_{r1}{c1}')
                    self.model.Add(self.cell_vars[(r1, c1)] == self.cell_vars[(r2, c2)]).OnlyEnforceIf(b_cell_eq_v)
                    self.model.Add(self.cell_vars[(r1, c1)] != self.cell_vars[(r2, c2)]).OnlyEnforceIf(b_cell_eq_v.Not())

                    self.model.AddImplication(b_region_eq_v, b_cell_eq_v)
                    self.model.AddImplication(b_cell_eq_v, b_region_eq_v)
