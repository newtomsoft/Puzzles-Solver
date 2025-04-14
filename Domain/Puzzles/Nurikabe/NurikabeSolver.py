from typing import Set

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class NurikabeSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 5 or self.columns_number < 5:
            raise ValueError("The grid must be at least 5x5")
        self.islands_area = [cell for row in self._grid.matrix for cell in row if cell > 0]
        self.island_count = len(self.islands_area)
        self.islands_area_position = [Position(r, c) for r in range(self.rows_number) for c in range(self.columns_number) if self._grid.value(r, c) > 0]
        self._solver = solver_engine
        self._grid_z3 = None

    def get_solution(self) -> (Grid, int):
        self._grid_z3 = Grid([[self._solver.bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        # True if a cell is black (river), False if white (island)
        self._add_constraints()
        solution = self._ensure_all_black_connected_and_no_island_without_number()
        return solution

    def get_other_solution(self):
        self._exclude_solution(self._previous_solution)
        return self._ensure_all_black_connected_and_no_island_without_number()

    def _exclude_solution(self, solution):
        rivers_cells = solution.get_all_shapes(1)
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[river_cell] for river_cells in rivers_cells for river_cell in river_cells])))

    def _ensure_all_black_connected_and_no_island_without_number(self):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[1 if self._solver.is_true(model.eval(self._grid_z3[Position(i, j)])) else 0 for j in range(self.columns_number)] for i in range(self.rows_number)])
            river_compliant = current_grid.are_cells_connected(1)
            islands = current_grid.get_all_shapes(0)
            if self._recompute_islands_without_island_area_or_wrong(islands):
                continue
            if river_compliant and len(islands) == self.island_count:
                self._previous_solution = current_grid
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
            not_all_cell_are_river = self._solver.Not(self._solver.And([self._grid_z3[position] for position in river]))
            around_river = ShapeGenerator.around_shape(river)
            around_river_are_not_all_island = self._solver.Not(self._solver.And([self._solver.Not(self._grid_z3[position]) for position in around_river if position in self._grid]))
            constraint = self._solver.Or(not_all_cell_are_river, around_river_are_not_all_island)
            self._solver.add(constraint)

    def _recompute_islands_without_island_area_or_wrong(self, islands):
        result = False
        for island in islands:
            if all(self._grid[position] == 0 for position in island) or any((island_area := self._grid[position]) != 0 for position in island) and island_area != len(island):
                black_around_shape = [position for position in ShapeGenerator.around_shape(island) if position in self._grid]
                blacks = [self._grid_z3[position] for position in black_around_shape]
                whites = [self._solver.Not(self._grid_z3[position]) for position in island]
                constraint_black_and_white = self._solver.And(blacks + whites)
                self._solver.add(self._solver.Not(constraint_black_and_white))
                result = True
        return result

    def _add_constraints(self):
        self._add_island_on_island_area_constraint()
        self._add_islands_area_sum_constraint()
        self._add_adjacent_1_is_river_constraint()
        self._add_river_between_2_island_area_constraint()
        self._add_river_if_2_island_area_diagonal_adjacent_constraint()
        self._add_no_square_river_constraint()
        self._add_islands_area_and_river_constraint()
        self._add_river_if_all_neighbors_river_and_not_island_area()

    def _add_island_on_island_area_constraint(self):
        constraint = [self._solver.Not(self._grid_z3[position]) for position in self.islands_area_position]
        self._solver.add(constraint)

    def _add_adjacent_1_is_river_constraint(self):
        for river_values in [self._grid_z3.neighbors_values(position) for position in self.islands_area_position if self._grid[position] == 1]:
            self._solver.add(river_values)

    def _add_islands_area_sum_constraint(self):
        islands_area_sum = sum(number for number in self.islands_area)
        constraint = sum(self._solver.Not(self._grid_z3[r][c]) for r in range(self.rows_number) for c in range(self.columns_number)) == islands_area_sum
        self._solver.add(constraint)

    def _add_no_square_river_constraint(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                if self._grid.value(r, c) == 0 and self._grid.value(r + 1, c) == 0 and self._grid.value(r, c + 1) == 0 and self._grid.value(r + 1, c + 1) == 0:
                    self._solver.add(self._solver.Not(self._solver.And(self._grid_z3[r][c], self._grid_z3[r + 1][c], self._grid_z3[r][c + 1], self._grid_z3[r + 1][c + 1])))

    def _add_islands_area_and_river_constraint(self):
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
            constraint_sum = sum(self._solver.Not(self._grid_z3[pos]) for pos in island_possible_positions) >= island_area
            self._solver.add(constraint_sum)
        return islands_possible_positions

    def _compute_possible_positions(self, possible_positions: set[Position], initial_position: Position, position: Position, island_area) -> Set[Position]:
        area = len(position - initial_position)
        if position != initial_position and self._grid[position] != 0 or area == island_area:
            return possible_positions
        adjacent_positions_to_add = {pos for pos in self._grid.neighbors_positions(position) if
                                     self._grid[pos] == 0 and pos not in possible_positions and not self._is_adjacent_with_other_island_area(pos, position)}
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

    def _add_river_between_2_island_area_constraint(self):
        for r in range(self.rows_number - 2):
            for c in range(self.columns_number - 2):
                position = Position(r, c)
                if self._grid[position] == 0:
                    continue
                neighbors = [position.after(Direction.down(), 2), position.after(Direction.right(), 2)]
                for river_value in [self._grid_z3[(neighbor_position + position) // 2] for neighbor_position in neighbors if self._grid[neighbor_position] != 0]:
                    self._solver.add(river_value)

    def _add_river_if_2_island_area_diagonal_adjacent_constraint(self):
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

    def _add_river_if_all_neighbors_river_and_not_island_area(self):
        for position, value in [(position, value) for position, value in self._grid_z3 if self._grid[position] == 0]:
            self._solver.Implies(self._solver.And([self._grid_z3[neighbor_position] for neighbor_position in self._grid.neighbors_positions(position)]), self._grid_z3[position])
