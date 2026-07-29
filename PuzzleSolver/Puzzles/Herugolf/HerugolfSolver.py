import random

from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class HerugolfSolver(GameSolver):
    cell_empty = None
    cell_water = 'W'
    cell_hole = 'H'

    _DIR_DELTAS = {
        1: (1, 0),
        2: (0, 1),
        3: (-1, 0),
        4: (0, -1),
    }

    _DIR_ARROWS = {
        1: '↓',
        2: '→',
        3: '↑',
        4: '←',
    }

    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self._previous_solution = None

    def get_solution(self) -> Grid:
        return self._solve_with_ortools()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return Grid.empty()
        return self._solve_with_ortools(block_solution=self._previous_solution)

    def _solve_with_ortools(self, block_solution: Grid | None = None) -> Grid:
        balls = []
        holes = []
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                val = self._grid.value(r, c)
                if isinstance(val, int) and val > 0:
                    balls.append((Position(r, c), val))
                elif val == self.cell_hole:
                    holes.append((r, c))

        if len(balls) != len(holes):
            return Grid.empty()

        forbidden = {
            (pos.r, pos.c) for (pos, _) in balls
        }
        forbidden.update(holes)
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if self._grid.value(r, c) == self.cell_water:
                    forbidden.add((r, c))

        balls = sorted(balls, key=lambda x: -x[1])
        R = self._grid.rows_number
        C = self._grid.columns_number

        all_paths = []
        path_index = 0
        ball_path_ids = {i: [] for i in range(len(balls))}
        hole_path_ids = {j: [] for j in range(len(holes))}
        cell_path_ids = {}

        def _record_path(path, ball_idx, hole_idx):
            nonlocal path_index
            covered_cells = set()
            for _, seg in path:
                for cell in seg:
                    if cell != (balls[ball_idx][0].r, balls[ball_idx][0].c):
                        covered_cells.add(cell)
            all_paths.append((ball_idx, hole_idx, path, covered_cells))
            ball_path_ids[ball_idx].append(path_index)
            hole_path_ids[hole_idx].append(path_index)
            for cell in covered_cells:
                cell_path_ids.setdefault(cell, []).append(path_index)
            path_index += 1

        def _find_paths(start, target, power, occupied):
            results = []
            stack = [(start, power, [])]
            while stack:
                pos, rem, path = stack.pop()
                if (pos.r, pos.c) == target:
                    results.append(path)
                    continue
                if rem == 0:
                    continue
                for code, (dr, dc) in self._DIR_DELTAS.items():
                    nr = pos.r + dr * rem
                    nc = pos.c + dc * rem
                    if not (0 <= nr < R and 0 <= nc < C):
                        continue
                    nxt = (nr, nc)
                    cells = []
                    ok = True
                    if dr != 0:
                        step = 1 if dr > 0 else -1
                        for rr in range(pos.r + step, nr, step):
                            if (rr, pos.c) in forbidden or (rr, pos.c) in occupied:
                                ok = False
                                break
                            cells.append((rr, pos.c))
                    else:
                        step = 1 if dc > 0 else -1
                        for cc in range(pos.c + step, nc, step):
                            if (pos.r, cc) in forbidden or (pos.r, cc) in occupied:
                                ok = False
                                break
                            cells.append((pos.r, cc))
                    if not ok:
                        continue
                    if nxt != target and (nxt in forbidden or nxt in occupied):
                        continue
                    used = set()
                    for _, seg in path:
                        used.update(seg)
                    new_seg = [(pos.r, pos.c)] + cells + [(nr, nc)]
                    overlap = False
                    for cell in new_seg:
                        if cell == (pos.r, pos.c):
                            continue
                        if cell in used:
                            overlap = True
                            break
                    if overlap:
                        continue
                    stack.append((Position(nr, nc), rem - 1, path + [(code, new_seg)]))
            return results

        for i, (start, power) in enumerate(balls):
            for j, hole in enumerate(holes):
                paths = _find_paths(start, hole, power, frozenset())
                for path in paths:
                    _record_path(path, i, j)

        if not all_paths:
            return Grid.empty()

        model = cp_model.CpModel()
        path_vars = [model.NewBoolVar(f"path_{p}") for p in range(len(all_paths))]

        for i in range(len(balls)):
            model.Add(sum(path_vars[p] for p in ball_path_ids[i]) == 1)

        for j in range(len(holes)):
            model.Add(sum(path_vars[p] for p in hole_path_ids[j]) == 1)

        for cell, ids in cell_path_ids.items():
            model.Add(sum(path_vars[p] for p in ids) <= 1)

        if block_solution is not None:
            for i, (ball_idx, _, path, _) in enumerate(all_paths):
                code, _ = path[0]
                if block_solution.value(balls[ball_idx][0].r, balls[ball_idx][0].c) == code:
                    model.Add(path_vars[i] == 0)

        solver = cp_model.CpSolver()
        solver.parameters.random_seed = 42
        if solver.Solve(model) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        out = [row[:] for row in self._grid.matrix]
        for i, (ball_idx, _, path, _) in enumerate(all_paths):
            if solver.Value(path_vars[i]):
                for code, seg in path:
                    for r, c in seg:
                        if self._grid.value(r, c) != self.cell_hole:
                            out[r][c] = self._DIR_ARROWS[code]

        solution_grid = Grid(out)
        self._previous_solution = solution_grid
        return solution_grid
