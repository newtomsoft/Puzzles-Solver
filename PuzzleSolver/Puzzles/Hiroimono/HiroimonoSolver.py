from ortools.sat.python import cp_model
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver

class HiroimonoSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._stones = []
        for r in range(grid.rows_number):
            for c in range(grid.columns_number):
                if grid.value(r, c) == 'S':
                    self._stones.append((r, c))
        self._n = len(self._stones)
        self._solution_path = []

    def get_solution(self) -> Grid:
        if not self._stones:
            return Grid.empty()
            
        path_indices = self._solve_ortools()
            
        if path_indices:
            self._solution_path = path_indices
            res_grid = Grid([[None for _ in range(self._grid.columns_number)] for _ in range(self._grid.rows_number)])
            for step, idx in enumerate(path_indices):
                r, c = self._stones[idx]
                res_grid.set_value(Position(r, c), step + 1)
            return res_grid
            
        return Grid.empty()

    def _solve_ortools(self):
        model = cp_model.CpModel()
        n = self._n
        
        # next_stone[i] = index of the stone picked at step i (0 to n-1)
        next_stone = [model.new_int_var(0, n - 1, f'next_stone_{i}') for i in range(n)]
        
        # order[s] = step at which stone s is picked (0 to n-1)
        order = [model.new_int_var(0, n - 1, f'order_{s}') for s in range(n)]
        
        model.add_all_different(next_stone)
        model.add_all_different(order)
        for i in range(n):
            model.add_element(next_stone[i], order, i)
        for s in range(n):
            model.add_element(order[s], next_stone, s)

        rels = {}
        for i in range(n):
            ri, ci = self._stones[i]
            for j in range(n):
                if i == j: continue
                rj, cj = self._stones[j]
                if ri == rj:
                    rels[(i, j)] = (1, 1 if cj > ci else -1)
                elif ci == cj:
                    rels[(i, j)] = (2, 1 if rj > ri else -1)

        between = {}
        for i in range(n):
            for j in range(n):
                if (i, j) not in rels: continue
                ri, ci, rj, cj = self._stones[i][0], self._stones[i][1], self._stones[j][0], self._stones[j][1]
                stones_between = []
                for k in range(n):
                    if k == i or k == j: continue
                    rk, ck = self._stones[k]
                    if ri == rj == rk and min(ci, cj) < ck < max(ci, cj):
                        stones_between.append(k)
                    elif ci == cj == ck and min(ri, rj) < rk < max(ri, rj):
                        stones_between.append(k)
                between[(i, j)] = stones_between

        # 1. Alignment and 3. No U-turns
        for i in range(n - 1):
            curr_s, next_s = next_stone[i], next_stone[i + 1]
            allowed_moves = [[s1, s2] for (s1, s2) in rels]
            model.add_allowed_assignments([curr_s, next_s], allowed_moves)
            
            if i > 0:
                prev_s = next_stone[i - 1]
                allowed_triplets = []
                for (s1, s2), (ax1, sg1) in rels.items():
                    for s3 in range(n):
                        if (s2, s3) in rels:
                            ax2, sg2 = rels[(s2, s3)]
                            if not (ax1 == ax2 and sg1 == -sg2):
                                allowed_triplets.append([s1, s2, s3])
                model.add_allowed_assignments([prev_s, curr_s, next_s], allowed_triplets)

        # 2. Intermediate stones
        for (s1, s2), intermediate in between.items():
            if not intermediate: continue
            for i in range(n - 1):
                # (next_stone[i] == s1 AND next_stone[i+1] == s2) => order[k] < i
                move_i = model.new_bool_var(f'm_{i}_{s1}_{s2}')
                s1_at_i, s2_at_ip1 = model.new_bool_var(f's1_{i}_{s1}'), model.new_bool_var(f's2_{i+1}_{s2}')
                model.add(next_stone[i] == s1).only_enforce_if(s1_at_i)
                model.add(next_stone[i] != s1).only_enforce_if(s1_at_i.negated())
                model.add(next_stone[i+1] == s2).only_enforce_if(s2_at_ip1)
                model.add(next_stone[i+1] != s2).only_enforce_if(s2_at_ip1.negated())
                model.add_bool_and([s1_at_i, s2_at_ip1]).only_enforce_if(move_i)
                model.add_bool_or([s1_at_i.negated(), s2_at_ip1.negated()]).only_enforce_if(move_i.negated())
                for k in intermediate:
                    model.add(order[k] < i).only_enforce_if(move_i)

        solver = cp_model.CpSolver()
        if solver.solve(model) in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return [solver.value(next_stone[i]) for i in range(n)]
        return []

    def debug_graph(self):
        print(f"Stones ({self._n}): {self._stones}")

    def get_other_solution(self) -> Grid:
        return Grid.empty()

    def print_solution(self):
        if not self._solution_path:
            print("No solution found")
            return
            
        print(f"Solution found with {len(self._solution_path)} stones:")
        for step, idx in enumerate(self._solution_path):
            r, c = self._stones[idx]
            print(f"{step+1:2d}: ({r}, {c})")
