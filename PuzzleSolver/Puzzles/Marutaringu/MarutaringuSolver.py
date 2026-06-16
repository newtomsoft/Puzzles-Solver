from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.GridMask import is_outside_region, resolve_outside
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class MarutaringuSolver(GameSolver):
    def __init__(self, regions_grid: Grid, clues_grid: Grid):
        super().__init__()
        self._regions_grid = regions_grid
        self.rows = regions_grid.rows_number
        self.cols = regions_grid.columns_number
        self._outside = resolve_outside(clues_grid)

        regions_dict = regions_grid.get_regions()
        self.regions = [
            [(pos.r, pos.c) for pos in cells]
            for _, cells in regions_dict.items()
            if not is_outside_region(cells, self._outside)
        ]

        self.clues = {}
        if clues_grid is not None:
            pos_to_region_idx = {}
            for idx, cells in enumerate(self.regions):
                for r, c in cells:
                    pos_to_region_idx[(r, c)] = idx
            for position, value in clues_grid:
                if value != 0 and value != GameSolver.cell_outside:
                    self.clues[pos_to_region_idx[(position.r, position.c)]] = value

        self.model = cp_model.CpModel()

        # B[r,c] = 1 if cell (r,c) is black
        self.b = {}
        for r in range(self.rows):
            for c in range(self.cols):
                self.b[r, c] = self.model.NewBoolVar(f'b_{r}_{c}')

        self._add_outside_constraints()
        self._add_degree_constraints()
        self._add_rectangle_constraints()
        self._add_no_2x2_constraint()
        self._previous_solution = None

    def _add_outside_constraints(self):
        for r, c in self._outside:
            self.model.Add(self.b[r, c] == 0)

    def _add_degree_constraints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self._outside:
                    continue
                neighbors = []
                if r > 0 and (r - 1, c) not in self._outside:
                    neighbors.append(self.b[r - 1, c])
                if r < self.rows - 1 and (r + 1, c) not in self._outside:
                    neighbors.append(self.b[r + 1, c])
                if c > 0 and (r, c - 1) not in self._outside:
                    neighbors.append(self.b[r, c - 1])
                if c < self.cols - 1 and (r, c + 1) not in self._outside:
                    neighbors.append(self.b[r, c + 1])

                # If b[r,c] is True, exactly 2 neighbors are True
                self.model.Add(sum(neighbors) == 2).OnlyEnforceIf(self.b[r, c])

    def _add_rectangle_constraints(self):
        for i, reg in enumerate(self.regions):
            reg_set = set(reg)
            min_reg_r = min(r for r, c in reg)
            max_reg_r = max(r for r, c in reg)
            min_reg_c = min(c for r, c in reg)
            max_reg_c = max(c for r, c in reg)

            valid_rectangles = []
            for r1 in range(min_reg_r, max_reg_r + 1):
                for r2 in range(r1, max_reg_r + 1):
                    for c1 in range(min_reg_c, max_reg_c + 1):
                        for c2 in range(c1, max_reg_c + 1):
                            rect_cells = []
                            is_contained = True
                            for r in range(r1, r2 + 1):
                                for c in range(c1, c2 + 1):
                                    if (r, c) not in reg_set:
                                        is_contained = False
                                        break
                                    rect_cells.append((r, c))
                                if not is_contained:
                                    break

                            if is_contained:
                                if i in self.clues:
                                    if len(rect_cells) == self.clues[i]:
                                        valid_rectangles.append(rect_cells)
                                else:
                                    if len(rect_cells) >= 1:
                                        valid_rectangles.append(rect_cells)

            # Exactly one of these rectangles must be chosen
            rect_bools = []
            for j, rect in enumerate(valid_rectangles):
                rb = self.model.NewBoolVar(f'reg_{i}_rect_{j}')
                rect_bools.append(rb)

                # If rb is true, then all cells in rect are black and others in region are white
                rect_set = set(rect)
                for r, c in reg:
                    if (r, c) in rect_set:
                        self.model.AddImplication(rb, self.b[r, c])
                    else:
                        self.model.AddImplication(rb, self.b[r, c].Not())

            self.model.AddExactlyOne(rect_bools)

    def _add_no_2x2_constraint(self):
        for r in range(self.rows - 1):
            for c in range(self.cols - 1):
                self.model.AddBoolOr([
                    self.b[r, c].Not(),
                    self.b[r + 1, c].Not(),
                    self.b[r, c + 1].Not(),
                    self.b[r + 1, c + 1].Not(),
                ])

    def get_solution(self) -> Grid:
        while True:
            status = self._solver.Solve(self.model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return Grid.empty()

            res = [[False for _ in range(self.cols)] for _ in range(self.rows)]
            black_cells = []
            for r in range(self.rows):
                for c in range(self.cols):
                    if self._solver.Value(self.b[r, c]) == 1:
                        res[r][c] = True
                        black_cells.append((r, c))

            if not black_cells:
                return Grid.empty()

            if self._is_connected(black_cells):
                self._previous_solution = res
                return Grid([[1 if res[r][c] else 0 for c in range(self.cols)] for r in range(self.rows)])
            else:
                comp = self._get_one_component(black_cells)
                self.model.AddBoolOr([self.b[r, c].Not() for r, c in comp])

    def _is_connected(self, black_cells):
        if not black_cells:
            return True
        comp = self._get_one_component(black_cells)
        return len(comp) == len(black_cells)

    @staticmethod
    def _get_one_component(black_cells):
        if not black_cells:
            return set()
        start = black_cells[0]
        visited = {start}
        stack = [start]
        black_set = set(black_cells)
        while stack:
            r, c = stack.pop()
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in black_set and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc))
        return visited

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        # Forbid previous solution
        clause = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self._previous_solution[r][c]:
                    clause.append(self.b[r, c].Not())
                else:
                    clause.append(self.b[r, c])
        self.model.AddBoolOr(clause)
        return self.get_solution()
