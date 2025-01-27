from typing import Set

from z3 import Solver, And, sat, Or, Bool, Not, is_true

from Utils.Grid import Grid
from Utils.Position import Position
from Utils.ShapeGenerator import ShapeGenerator


class NurikabeGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 5 or self.columns_number < 5:
            raise ValueError("The grid must be at least 5x5")
        self.islands_area = [cell for row in self._grid.matrix for cell in row if cell > 0]
        self.island_count = len(self.islands_area)
        self.islands_area_position = [Position(r, c) for r in range(self.rows_number) for c in range(self.columns_number) if self._grid.value(r, c) > 0]
        self._solver = None
        self._grid_z3 = None

    def get_solution(self) -> (Grid, int):
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
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
        self._solver.add(Not(And([self._grid_z3[r][c] for river_cell in river_cells for r, c in river_cell])))

    def _ensure_all_black_connected_and_no_island_without_number(self):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[1 if is_true(model.eval(self._grid_z3[Position(i, j)])) else 0 for j in range(self.columns_number)] for i in range(self.rows_number)])
            river_compliant = current_grid.are_all_cells_connected(1)
            islands = current_grid.get_all_shapes(0)
            if self._recompute_islands_without_island_area_or_wrong(islands):
                continue
            if river_compliant and len(islands) == self.island_count:
                self._last_solution = current_grid
                return current_grid

            if not river_compliant:
                self._recompute_river(current_grid)
            if len(islands) > self.island_count:
                self._recompute_islands_without_island_area_or_wrong(islands)
            if len(islands) < self.island_count:
                self._exclude_solution(current_grid)

        return Grid.empty()

    def _recompute_river(self, grid):
        rivers = grid.get_all_shapes(1)
        biggest_river = max(rivers, key=len)
        rivers.remove(biggest_river)
        for river in rivers:
            not_all_cell_are_river = Not(And([self._grid_z3[position] for position in river]))
            around_river = ShapeGenerator.around_shape(river)
            around_river_are_not_all_island = Not(And([Not(self._grid_z3[position]) for position in around_river if 0 <= position.r < self.rows_number and 0 <= position.c < self.columns_number]))
            constraint = Or(not_all_cell_are_river, around_river_are_not_all_island)
            self._solver.add(constraint)

    def _recompute_islands_without_island_area_or_wrong(self, islands):
        result = False
        for island in islands:
            if all(self._grid[position] == 0 for position in island) or any((island_area := self._grid[position]) != 0 for position in island) and island_area != len(island):
                black_around_shape = [position for position in ShapeGenerator.around_shape(island) if 0 <= position.r < self.rows_number and 0 <= position.c < self.columns_number]
                blacks = [self._grid_z3[position] for position in black_around_shape]
                whites = [Not(self._grid_z3[position]) for position in island]
                constraint_black_and_white = And(blacks + whites)
                self._solver.add(Not(constraint_black_and_white))
                result = True
        return result

    def _add_constraints(self):
        self._constraint_island_on_island_area()
        self._constraint_islands_area_sum()
        self._constraint_adjacent_1_is_river()
        self._constraint_river_between_2_island_area()
        self._constraint_river_if_2_island_area_diagonal_adjacent()
        self._constraint_no_square_river()
        self._constraint_islands_area_and_river()

    def _constraint_island_on_island_area(self):
        constraint = [Not(self._grid_z3[position]) for position in self.islands_area_position]
        self._solver.add(constraint)

    def _constraint_adjacent_1_is_river(self):
        for river_values in [self._grid_z3.neighbors_values(position) for position in self.islands_area_position if self._grid[position] == 1]:
            self._solver.add(river_values)

    def _constraint_islands_area_sum(self):
        islands_area_sum = sum(number for number in self.islands_area)
        constraint = sum(Not(self._grid_z3[r][c]) for r in range(self.rows_number) for c in range(self.columns_number)) == islands_area_sum
        self._solver.add(constraint)

    def _constraint_no_square_river(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                if self._grid.value(r, c) == 0 and self._grid.value(r + 1, c) == 0 and self._grid.value(r, c + 1) == 0 and self._grid.value(r + 1, c + 1) == 0:
                    self._solver.add(Not(And(self._grid_z3[r][c], self._grid_z3[r + 1][c], self._grid_z3[r][c + 1], self._grid_z3[r + 1][c + 1])))

    def _constraint_islands_area_and_river(self):
        islands_possible_positions = self._constraint_islands_area()
        self._constraint_must_be_river(islands_possible_positions)

    def _constraint_islands_area(self):  # todo improve
        islands_possible_positions = set()
        for initial_position in self.islands_area_position:
            island_area = self._grid[initial_position]
            island_possible_positions = set()
            island_possible_positions.add(initial_position)
            island_possible_positions = self._compute_possible_positions(island_possible_positions, initial_position, initial_position, island_area)
            islands_possible_positions.update(island_possible_positions)
            constraint_sum = sum(Not(self._grid_z3[pos]) for pos in island_possible_positions) >= island_area
            self._solver.add(constraint_sum)
        return islands_possible_positions

    def _compute_possible_positions(self, possible_positions: set[Position], initial_position: Position, position: Position, island_area) -> Set[Position]:
        area = len(position - initial_position)
        if position != initial_position and self._grid[position] != 0 or area == island_area:
            return possible_positions
        adjacent_positions_to_add = {pos for pos in self._grid.neighbors_positions(position) if self._grid[pos] == 0 and pos not in possible_positions and not self._is_adjacent_with_other_island_area(pos, position)}
        if len(adjacent_positions_to_add) == 0:
            return possible_positions
        possible_positions.update(adjacent_positions_to_add)
        for current_position in adjacent_positions_to_add:
            possible_positions = self._compute_possible_positions(possible_positions, initial_position, current_position, island_area)
        return possible_positions

    def _constraint_must_be_river(self, islands_possible_positions):
        for _, river_value in ((position, river_value) for position, river_value in self._grid_z3 if position not in islands_possible_positions):
            self._solver.add(river_value)

    def _is_adjacent_with_other_island_area(self, position: Position, position_origin: Position):
        return any([self._grid[adjacent_position] for adjacent_position in self._grid.neighbors_positions(position) if adjacent_position != position_origin]) > 0

    def _constraint_river_between_2_island_area(self):
        for r in range(self.rows_number - 2):
            for c in range(self.columns_number - 2):
                position = Position(r, c)
                if self._grid[position] == 0:
                    continue
                neighbors = [position + position_offset for position_offset in [Position(2, 0), Position(0, 2)]]
                for river_value in [self._grid_z3[(neighbor_position + position) // 2] for neighbor_position in neighbors if self._grid[neighbor_position] != 0]:
                    self._solver.add(river_value)

    def _constraint_river_if_2_island_area_diagonal_adjacent(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                if self._grid.value(r, c) == 0 or self._grid.value(r + 1, c + 1) == 0:
                    continue
                self._solver.add(self._grid_z3[r + 1][c])
                self._solver.add(self._grid_z3[r][c + 1])

        for r in range(self.rows_number - 1):
            for c in range(1, self.columns_number):
                if self._grid.value(r, c) == 0 or self._grid.value(r + 1, c - 1) == 0:
                    continue
                self._solver.add(self._grid_z3[r + 1][c])
                self._solver.add(self._grid_z3[r][c - 1])
