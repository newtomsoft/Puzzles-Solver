from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.GameSolver import GameSolver


class YonmasuSolver(GameSolver):
    empty = '.'
    forbidden = '#'
    circle = 'O'

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._rows = grid.rows_number
        self._cols = grid.columns_number
        self._o_positions = [Position(r, c) for r in range(self._rows) for c in range(self._cols) if grid[r, c] == self.circle]
        self._hash_positions = [Position(r, c) for r in range(self._rows) for c in range(self._cols) if grid[r, c] == self.forbidden]
        self._o_count = len(self._o_positions)
        self._hash_count = len(self._hash_positions)
        self._all_tetrominoes_per_o = self._generate_tetrominoes()
        self._model = cp_model.CpModel()
        self._tetro_vars = None
        self._solver = cp_model.CpSolver()
        self._previous_solution = None

    def _get_tetrominoes_containing(self, o_pos: Position) -> list[frozenset[Position]]:
        result = []
        start = o_pos
        self._dfs_find_4_cells(start, start, {start}, result)
        return result

    def _dfs_find_4_cells(self, o_pos: Position, current: Position, cells: set[Position], result: list[frozenset[Position]]):
        if len(cells) == 4:
            result.append(frozenset(cells))
            return
        visited_order = list(cells)
        for pos in visited_order:
            for neighbor in pos.neighbors():
                if neighbor in cells or neighbor in self._hash_set or not self._is_valid_cell(neighbor):
                    continue
                cells.add(neighbor)
                self._dfs_find_4_cells(o_pos, neighbor, cells, result)
                cells.remove(neighbor)

    def _generate_tetrominoes(self):
        self._hash_set = set(self._hash_positions)
        result = []
        for o_pos in self._o_positions:
            placements = list(set(self._get_tetrominoes_containing(o_pos)))
            result.append(placements)
        return result

    def _is_valid_cell(self, pos: Position) -> bool:
        return 0 <= pos.r < self._rows and 0 <= pos.c < self._cols

    def get_solution(self) -> Grid:
        self._init_vars()
        self._init_constraints()
        self._solver.parameters.max_time_in_seconds = 30
        status = self._solver.solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        solution = self._build_solution()
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> RegionsGrid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return RegionsGrid.empty()

        literals = []
        for i, placements in enumerate(self._all_tetrominoes_per_o):
            for p_idx in range(len(placements)):
                if self._solver.value(self._tetro_vars[i][p_idx]):
                    literals.append(self._tetro_vars[i][p_idx].negated())

        if literals:
            self._model.add_bool_or(literals)

        status = self._solver.solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return RegionsGrid.empty()

        solution = self._build_solution()
        self._previous_solution = solution
        return solution

    def _init_vars(self):
        self._tetro_vars = []
        for i in range(self._o_count):
            o_vars = [self._model.new_bool_var(f"tetro_{i}_{j}") for j in range(len(self._all_tetrominoes_per_o[i]))]
            self._tetro_vars.append(o_vars)

    def _init_constraints(self):
        for i in range(self._o_count):
            self._model.add(sum(self._tetro_vars[i]) == 1)

        cell_covered = {Position(r, c): [] for r in range(self._rows) for c in range(self._cols) if self._input_grid[r, c] != self.forbidden}
        for i, placements in enumerate(self._all_tetrominoes_per_o):
            for p_idx, cells in enumerate(placements):
                for cell in cells:
                    cell_covered[cell].append(self._tetro_vars[i][p_idx])

        for cell, vars_covering in cell_covered.items():
            self._model.add(sum(vars_covering) == 1)

    def _build_solution(self) -> RegionsGrid:
        solution = [[None for _ in range(self._cols)] for _ in range(self._rows)]

        for j, pos in enumerate(self._hash_positions):
            solution[pos.r][pos.c] = self._o_count + j

        for i, placements in enumerate(self._all_tetrominoes_per_o):
            for p_idx, cells in enumerate(placements):
                if self._solver.value(self._tetro_vars[i][p_idx]):
                    for cell in cells:
                        solution[cell.r][cell.c] = i

        return RegionsGrid(solution)
