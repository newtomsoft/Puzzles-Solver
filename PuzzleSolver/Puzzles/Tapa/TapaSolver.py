from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class TapaSolver(GameSolver):
    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 2 or self.columns_number < 2:
            raise ValueError("The grid must be at least 2x2")
        if not any(isinstance(cell, list) for row in self._grid.matrix for cell in row):
            raise ValueError("The grid must contain at least one list number")
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = self._build_solution()
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        terms = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                var = self._grid_vars.value(r + 1, c + 1)
                if self._previous_solution.value(r, c):
                    terms.append(var.negated())
                else:
                    terms.append(var)
        self._model.add_bool_or(terms)

        return self.get_solution()

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_bool_var(f"c_{r}_{c}") for c in range(self._grid.columns_number + 2)] for r in range(self._grid.rows_number + 2)])
        self._init_adjacent_cells()
        self._init_borders_white()
        self._no_black_on_numbers_cell()
        self._black_around_number()
        self._no_black_square()
        self._add_black_connectivity_constraint()

    def _build_solution(self) -> Grid:
        return Grid([[True if self._solver.boolean_value(self._grid_vars.value(r + 1, c + 1)) else False for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])

    def _init_borders_white(self):
        for r in range(self._grid_vars.rows_number):
            self._model.add(self._grid_vars.value(r, 0) == 0)
            self._model.add(self._grid_vars.value(r, self._grid_vars.columns_number - 1) == 0)
        for c in range(self._grid_vars.columns_number):
            self._model.add(self._grid_vars.value(0, c) == 0)
            self._model.add(self._grid_vars.value(self._grid_vars.rows_number - 1, c) == 0)

    def _no_black_on_numbers_cell(self):
        for position in [position for position, value in self._grid if value != 0]:
            self._model.add(self._grid_vars[position + Position(1, 1)] == 0)

    def _black_around_number(self):
        neighbours_adjacent_coordinates = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                neighbours_black_counts = self._grid.value(r, c)
                if not isinstance(neighbours_black_counts, list):
                    continue
                black_cells_around = [self._grid_vars.value(r + 1 + dr, c + 1 + dc) for dr, dc in neighbours_adjacent_coordinates]
                if any(count > 8 or count < 0 for count in neighbours_black_counts):
                    raise ValueError("Number must be positive and less than 9")
                adjacent_combinations = []
                for neighbours_black_count in neighbours_black_counts:
                    adjacent_combination = self.adjacent_cells[neighbours_black_count]
                    adjacent_combinations.append(adjacent_combination)
                merged_combinations = TapaSolver._combine_list_with_gap(adjacent_combinations)
                combo_vars = []
                for idx, combination in enumerate(merged_combinations):
                    cv = self._model.new_bool_var(f"combo_{r}_{c}_{idx}")
                    combo_terms = []
                    for i, is_black in enumerate(combination):
                        term = black_cells_around[i] if is_black else black_cells_around[i].negated()
                        self._model.add_implication(cv, term)
                        combo_terms.append(term)
                    self._model.add_bool_or([t.negated() for t in combo_terms] + [cv])
                    combo_vars.append(cv)
                self._model.add_bool_or(combo_vars)

    def _no_black_square(self):
        for c in range(1, self._grid_vars.columns_number - 1):
            for r in range(1, self._grid_vars.rows_number - 1):
                self._model.add_bool_or([
                    self._grid_vars.value(r, c).negated(),
                    self._grid_vars.value(r + 1, c).negated(),
                    self._grid_vars.value(r, c + 1).negated(),
                    self._grid_vars.value(r + 1, c + 1).negated()
                ])

    def _add_black_connectivity_constraint(self):
        total_cells = self._grid_vars.rows_number * self._grid_vars.columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self._grid_vars.columns_number)] for r in range(self._grid_vars.rows_number)])
        is_root_vars = []
        for r in range(self._grid_vars.rows_number):
            for c in range(self._grid_vars.columns_number):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                is_black = self._grid_vars[pos]
                self._model.add(is_root <= is_black)
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self._grid_vars.rows_number):
            for c in range(self._grid_vars.columns_number):
                pos = Position(r, c)
                is_black = self._grid_vars[pos]
                is_root = is_root_vars[r * self._grid_vars.columns_number + c]
                parent_literals = []
                for neighbor in self._grid_vars.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 1).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_black, is_root.negated()])

    def _init_adjacent_cells(self):
        neighbors_count = 8
        self.adjacent_cells = {cells_count: Grid.get_adjacent_combinations(neighbors_count, cells_count, True) for cells_count in range(neighbors_count + 1)}

    @staticmethod
    def _combine_with_gap(blocks1: list[list[bool]], blocks2: list[list[bool]]) -> list[list[bool]]:
        true_count = blocks1[0].count(True) + blocks2[0].count(True)
        block_count = TapaSolver._adjacent_group_count(blocks1[0]) + TapaSolver._adjacent_group_count(blocks2[0])
        if len(blocks1[0]) != len(blocks2[0]):
            return []
        neighbour_length = len(blocks1[0])
        result = []
        for adjacent1 in blocks1:
            for adjacent2 in blocks2:
                combined = [adjacent1[i] ^ adjacent2[i] for i in range(len(adjacent1))]
                if combined.count(True) != true_count or combined in result:
                    continue
                combo = [i for i in range(len(combined)) if combined[i]]
                cell_adjacent = [True for i in range(1, len(combo)) if combo[i] - combo[i - 1] == 1]
                if combo[0] + neighbour_length - combo[-1] == 1:
                    cell_adjacent.append(True)
                if TapaSolver._adjacent_group_count(combined) == block_count:
                    result.append(combined)
        return result

    @staticmethod
    def _combine_list_with_gap(blocks_list: list[list[list[bool]]]) -> list[list[bool]]:
        if len(blocks_list) == 1:
            return blocks_list[0]
        if len(blocks_list) == 2:
            return TapaSolver._combine_with_gap(blocks_list[0], blocks_list[1])
        result = TapaSolver._combine_list_with_gap([TapaSolver._combine_with_gap(blocks_list[0], blocks_list[1])] + blocks_list[2:])
        return result

    @staticmethod
    def _adjacent_group_count(combination: list[bool]):
        return combination.count(True) - TapaSolver._adjacent_count(combination)

    @staticmethod
    def _adjacent_count(block: list[bool]):
        return sum(block[i] and block[i + 1] for i in range(len(block) - 1)) + (block[0] and block[-1])
