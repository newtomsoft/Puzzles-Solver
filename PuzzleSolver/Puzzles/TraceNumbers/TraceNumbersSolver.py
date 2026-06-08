from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class TraceNumbersSolver(GameSolver):
    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self.rows_number = grid.rows_number
        self.columns_number = grid.columns_number
        self._previous_solution: Grid | None = None

    def _get_num_paths(self):
        count = 0
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == 1:
                    count += 1
        return count

    def _get_max_number(self):
        max_val = 0
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                v = self._grid.value(r, c)
                if v is not None and v > max_val:
                    max_val = v
        return max_val

    def get_solution(self) -> Grid:
        self._previous_solution = self._solve()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        return Grid.empty()

    def _solve(self) -> Grid:
        model = cp_model.CpModel()

        R = self.rows_number
        C = self.columns_number
        P = self._get_num_paths()
        N = R * C

        cell_path = [[model.NewIntVar(0, P - 1, f'p_{r}_{c}') for c in range(C)] for r in range(R)]
        cell_order = [[model.NewIntVar(0, N - 1, f'o_{r}_{c}') for c in range(C)] for r in range(R)]

        in_path = [[[model.NewBoolVar(f'in_{r}_{c}_{p}') for p in range(P)] for c in range(C)] for r in range(R)]
        for r in range(R):
            for c in range(C):
                for p in range(P):
                    model.Add(cell_path[r][c] == p).OnlyEnforceIf(in_path[r][c][p])
                    model.Add(cell_path[r][c] != p).OnlyEnforceIf(in_path[r][c][p].Not())

        max_num = self._get_max_number()
        for v in range(1, max_num + 1):
            cells_with_v = [(r, c) for r in range(R) for c in range(C) if self._grid.value(r, c) == v]
            for p in range(P):
                model.Add(sum(in_path[r][c][p] for r, c in cells_with_v) == 1)

        for r in range(R):
            for c in range(C):
                prev_bools = []
                next_bools = []

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < R and 0 <= nc < C):
                        continue

                    same = model.NewBoolVar(f'same_{r}_{c}_{nr}_{nc}')
                    model.Add(cell_path[r][c] == cell_path[nr][nc]).OnlyEnforceIf(same)
                    model.Add(cell_path[r][c] != cell_path[nr][nc]).OnlyEnforceIf(same.Not())

                    order_next_cond = model.NewBoolVar(f'onc_{r}_{c}_{nr}_{nc}')
                    model.Add(cell_order[nr][nc] == cell_order[r][c] + 1).OnlyEnforceIf(order_next_cond)
                    model.Add(cell_order[nr][nc] != cell_order[r][c] + 1).OnlyEnforceIf(order_next_cond.Not())

                    order_prev_cond = model.NewBoolVar(f'opc_{r}_{c}_{nr}_{nc}')
                    model.Add(cell_order[nr][nc] + 1 == cell_order[r][c]).OnlyEnforceIf(order_prev_cond)
                    model.Add(cell_order[nr][nc] + 1 != cell_order[r][c]).OnlyEnforceIf(order_prev_cond.Not())

                    is_next = model.NewBoolVar(f'nxt_{r}_{c}_{nr}_{nc}')
                    model.AddImplication(is_next, same)
                    model.AddImplication(is_next, order_next_cond)
                    model.AddBoolOr([is_next, same.Not(), order_next_cond.Not()])
                    next_bools.append(is_next)

                    is_prev = model.NewBoolVar(f'prv_{r}_{c}_{nr}_{nc}')
                    model.AddImplication(is_prev, same)
                    model.AddImplication(is_prev, order_prev_cond)
                    model.AddBoolOr([is_prev, same.Not(), order_prev_cond.Not()])
                    prev_bools.append(is_prev)

                model.Add(sum(next_bools) <= 1)
                model.Add(sum(prev_bools) <= 1)
                model.Add(sum(next_bools) + sum(prev_bools) >= 1)

        for v in range(1, max_num):
            cells_v = [(r, c) for r in range(R) for c in range(C) if self._grid.value(r, c) == v]
            cells_v1 = [(r, c) for r in range(R) for c in range(C) if self._grid.value(r, c) == v + 1]
            for p in range(P):
                for r1, c1 in cells_v:
                    for r2, c2 in cells_v1:
                        both = model.NewBoolVar(f'both_{r1}_{c1}_{r2}_{c2}_{p}')
                        model.Add(in_path[r1][c1][p] + in_path[r2][c2][p] == 2).OnlyEnforceIf(both)
                        model.Add(in_path[r1][c1][p] + in_path[r2][c2][p] != 2).OnlyEnforceIf(both.Not())
                        model.Add(cell_order[r1][c1] < cell_order[r2][c2]).OnlyEnforceIf(both)

        model.Maximize(cell_order[R - 1][C - 1])
        status = self._solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        return self._build_solution(cell_path, self._solver)

    def _build_solution(self, path_vars, solver):
        R = self.rows_number
        C = self.columns_number
        data = [[0 for _ in range(C)] for _ in range(R)]
        for r in range(R):
            for c in range(C):
                data[r][c] = self._solver.Value(path_vars[r][c])
        return Grid(data)
