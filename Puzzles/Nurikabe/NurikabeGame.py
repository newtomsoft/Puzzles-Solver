from z3 import Solver, And, sat, Or, Bool, Not, is_true

from Utils.Grid import Grid
from Utils.ShapeGenerator import ShapeGenerator


class NurikabeGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 5 or self.columns_number < 5:
            raise ValueError("The grid must be at least 5x5")
        self.islands_size = [cell for row in self._grid.matrix for cell in row if cell > 0]
        self.island_count = len(self.islands_size)
        self.islands_size_position = [(r, c) for r in range(self.rows_number) for c in range(self.columns_number) if self._grid.value(r, c) > 0]
        self._solver = None
        self._matrix_z3 = None

    def get_solution(self) -> (Grid, int):
        self._matrix_z3 = [[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        # True if a cell is black (river), False if white (island)
        self._solver = Solver()
        self._add_constraints()
        solution = self._ensure_all_black_connected_and_no_island_without_number()
        return solution

    def get_other_solution(self):
        self._exclude_solution(self._last_solution)
        solution = self._ensure_all_black_connected_and_no_island_without_number()
        return solution

    def _exclude_solution(self, solution):
        river_cells = solution.get_all_shapes(1)
        self._solver.add(Not(And([self._matrix_z3[r][c] for river_cell in river_cells for r, c in river_cell])))

    def _ensure_all_black_connected_and_no_island_without_number(self):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[1 if is_true(model.eval(self._matrix_z3[i][j])) else 0 for j in range(self.columns_number)] for i in range(self.rows_number)])
            river_compliant = current_grid.are_all_cells_connected(1)
            islands = current_grid.get_all_shapes(0)
            if self._recompute_islands_without_island_size_or_wrong(islands):
                continue
            if river_compliant and len(islands) == self.island_count:
                self._last_solution = current_grid
                return current_grid

            if not river_compliant:
                self._recompute_river(current_grid)
            if len(islands) > self.island_count:
                self._recompute_islands_without_island_size_or_wrong(islands)
            if len(islands) < self.island_count:
                self._exclude_solution(current_grid)

        return Grid.empty()

    def _recompute_river(self, grid):
        rivers = grid.get_all_shapes(1)
        biggest_river = max(rivers, key=len)
        rivers.remove(biggest_river)
        for river in rivers:
            not_all_cell_are_river = Not(And([self._matrix_z3[r][c] for r, c in river]))
            around_river = ShapeGenerator.around_shape(river)
            around_river_are_not_all_island = Not(And([Not(self._matrix_z3[r][c]) for (r, c) in around_river if 0 <= r < self.rows_number and 0 <= c < self.columns_number]))
            constraint = Or(not_all_cell_are_river, around_river_are_not_all_island)
            self._solver.add(constraint)

    def _recompute_islands_without_island_size_or_wrong(self, islands):
        result = False
        for island in islands:
            if all(self._grid.value(r, c) == 0 for r, c in island) or any((island_size := self._grid.value(r, c)) != 0 for r, c in island) and island_size != len(island):
                black_around_shape = [(r, c) for (r, c) in ShapeGenerator.around_shape(island) if 0 <= r < self.rows_number and 0 <= c < self.columns_number]
                blacks = [self._matrix_z3[r][c] for (r, c) in black_around_shape]
                whites = [Not(self._matrix_z3[r][c]) for (r, c) in island]
                blacks_and_whites = blacks + whites
                constraint_black_and_white = And(blacks_and_whites)
                self._solver.add(Not(constraint_black_and_white))
                result = True
        return result

    def _add_constraints(self):
        self._constraint_island_on_island_size()
        self._constraint_islands_size_sum()
        self._constraint_adjacent_1_is_river()
        self._constraint_river_between_2_island_size()
        self._constraint_river_if_2_island_size_diagonal_adjacent()
        self._constraint_no_square_river()
        self._constraint_islands_size_and_river()
        # self._force_solution()

    def _constraint_island_on_island_size(self):
        constraint = [Not(self._matrix_z3[r][c]) for r, c in self.islands_size_position]
        self._solver.add(constraint)

    def _constraint_adjacent_1_is_river(self):
        for r, c in self.islands_size_position:
            if self._grid.value(r, c) == 1:
                adjacents = self._adjacents(r, c)
                self._solver.add([self._matrix_z3[r][c] for (r, c) in adjacents])

    def _constraint_islands_size_sum(self):
        islands_size_sum = sum(number for number in self.islands_size)
        constraint = sum(Not(self._matrix_z3[r][c]) for r in range(self.rows_number) for c in range(self.columns_number)) == islands_size_sum
        self._solver.add(constraint)

    def _constraint_no_square_river(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                if self._grid.value(r, c) == 0 and self._grid.value(r + 1, c) == 0 and self._grid.value(r, c + 1) == 0 and self._grid.value(r + 1, c + 1) == 0:
                    self._solver.add(Not(And(self._matrix_z3[r][c], self._matrix_z3[r + 1][c], self._matrix_z3[r][c + 1], self._matrix_z3[r + 1][c + 1])))

    def _constraint_islands_size_and_river(self):
        islands_possible_positions = self._constraint_islands_size()
        self._constraint_must_be_river(islands_possible_positions)

    def _constraint_islands_size(self):
        islands_possible_positions = set()
        for r, c in self.islands_size_position:
            island_size = self._grid.value(r, c)
            initial_position = (r, c)
            island_possible_positions = set()
            island_possible_positions.add(initial_position)
            island_possible_positions = self._compute_possible_positions(island_possible_positions, initial_position, initial_position, island_size)
            islands_possible_positions.update(island_possible_positions)
            constraint_sum = sum(Not(self._matrix_z3[rn][cn]) for (rn, cn) in island_possible_positions) >= island_size
            self._solver.add(constraint_sum)
        return islands_possible_positions

    def _compute_possible_positions(self, possible_positions: set[(int, int)], initial_position, position, island_size):
        r_initial, c_initial = initial_position
        r, c = position
        dr, dc = abs(r - r_initial), abs(c - c_initial)
        size = dr + dc + 1
        if position != initial_position and self._grid.value(r, c) != 0 or size == island_size:
            return possible_positions
        adjacents_to_add = {position for position in self._adjacents(r, c, False) if position not in possible_positions and not self._is_adjacent_with_other_island_size(*position, r, c)}
        if len(adjacents_to_add) == 0:
            return possible_positions
        possible_positions.update(adjacents_to_add)
        for current_position in adjacents_to_add:
            possible_positions = self._compute_possible_positions(possible_positions, initial_position, current_position, island_size)
        return possible_positions

    def _adjacents(self, r, c, possible_on_island_size=True):
        adjacents = [
            (r + dr, c + dc)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= r + dr < self.rows_number and 0 <= c + dc < self.columns_number and (possible_on_island_size or self._grid.value(r + dr, c + dc) == 0)
        ]
        return adjacents

    def _constraint_must_be_river(self, islands_possible_positions):
        for r, c in ((r, c) for r in range(self.rows_number) for c in range(self.columns_number) if (r, c) not in islands_possible_positions):
            self._solver.add(self._matrix_z3[r][c])

    def _is_adjacent_with_other_island_size(self, r, c, r_origin, c_origin):
        adjacents = self._adjacents(r, c)
        for ra, ca in adjacents:
            if ra == r_origin and ca == c_origin:
                continue
            if self._grid.value(ra, ca) > 0:
                return True
        return False

    def _constraint_river_between_2_island_size(self):
        for r in range(self.rows_number - 2):
            for c in range(self.columns_number - 2):
                if self._grid.value(r, c) == 0:
                    continue
                neighbors = [(r + dr, c + dc) for dr, dc in [(2, 0), (0, 2)]]
                for rn, cn in neighbors:
                    if self._grid.value(rn, cn) == 0:
                        continue
                    r1 = r + 1 if rn != r else r
                    c1 = c + 1 if cn != c else c
                    self._solver.add(self._matrix_z3[r1][c1])

    def _constraint_river_if_2_island_size_diagonal_adjacent(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                if self._grid.value(r, c) == 0 or self._grid.value(r + 1, c + 1) == 0:
                    continue
                self._solver.add(self._matrix_z3[r + 1][c])
                self._solver.add(self._matrix_z3[r][c + 1])

        for r in range(self.rows_number - 1):
            for c in range(1, self.columns_number):
                if self._grid.value(r, c) == 0 or self._grid.value(r + 1, c - 1) == 0:
                    continue
                self._solver.add(self._matrix_z3[r + 1][c])
                self._solver.add(self._matrix_z3[r][c - 1])

    def _force_solution(self):
        matrix_solution = [
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
        ]
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if matrix_solution[r][c] == 1:
                    self._solver.add(self._matrix_z3[r][c])
                else:
                    self._solver.add(Not(self._matrix_z3[r][c]))
