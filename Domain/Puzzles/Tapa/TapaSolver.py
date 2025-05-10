from Board.Position import Position
from Domain.Board.Grid import Grid
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class TapaSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 2 or self.columns_number < 2:
            raise ValueError("The grid must be at least 2x2")
        if not any(isinstance(cell, list) for row in self._grid.matrix for cell in row):
            raise ValueError("The grid must contain at least one list number")
        self._solver = solver_engine
        self._grid_z3: Grid | None = None

    def get_solution(self) -> (Grid | None, int):
        matrix_z3 = [[self._solver.bool(f"bool_{r}_{c}") for c in range(1 + self._grid.columns_number + 1)] for r in range(1 + self._grid.rows_number + 1)]
        #  True for black, False for white
        self._grid_z3 = Grid(matrix_z3)

        self._init_borders_white()
        self._init_adjacent_cells()
        self._no_black_on_numbers_cell()
        self._black_around_number()
        self._no_black_square()

        solution, _ = self._ensure_all_black_connected()
        return solution

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def _init_borders_white(self):
        self._solver.add([self._solver.Not(self._grid_z3.value(r, 0)) for r in range(self._grid_z3.rows_number)])
        self._solver.add([self._solver.Not(self._grid_z3.value(r, self._grid_z3.columns_number - 1)) for r in range(self._grid_z3.rows_number)])
        self._solver.add([self._solver.Not(self._grid_z3.value(0, c)) for c in range(self._grid_z3.columns_number)])
        self._solver.add([self._solver.Not(self._grid_z3.value(self._grid_z3.rows_number - 1, c)) for c in range(self._grid_z3.columns_number)])

    def _no_black_on_numbers_cell(self):
        for position in [position for position, value in self._grid if value != 0]:
            self._solver.add(self._solver.Not(self._grid_z3[position + Position(1, 1)]))

    def _black_around_number(self):
        neighbours_adjacent_coordinates = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                neighbours_black_counts = self._grid.value(r, c)
                if not isinstance(neighbours_black_counts, list):
                    continue
                black_cells_around = [self._grid_z3.value(r + 1 + dr, c + 1 + dc) for dr, dc in neighbours_adjacent_coordinates]
                if any(count > 8 or count < 0 for count in neighbours_black_counts):
                    raise ValueError("Number must be positive and less than 9")
                adjacent_combinations = []
                for neighbours_black_count in neighbours_black_counts:
                    adjacent_combination = self.adjacent_cells[neighbours_black_count]
                    adjacent_combinations.append(adjacent_combination)
                merged_combinations = TapaSolver._combine_list_with_gap(adjacent_combinations)
                constraints = []
                for combination in merged_combinations:
                    constraints.append(self._solver.And([black_cells_around[i] if combination[i] else self._solver.Not(black_cells_around[i]) for i in range(len(combination))]))
                self._solver.add(self._solver.Or(constraints))

    def _no_black_square(self):
        for c in range(1, self._grid_z3.columns_number - 1):
            for r in range(1, self._grid_z3.rows_number - 1):
                self._solver.add(self._solver.Or(
                    self._solver.Not(self._grid_z3.value(r, c)),
                    self._solver.Not(self._grid_z3.value(r + 1, c)),
                    self._solver.Not(self._grid_z3.value(r, c + 1)),
                    self._solver.Not(self._grid_z3.value(r + 1, c + 1))
                ))

    def _ensure_all_black_connected(self) -> (Grid, int):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[self._solver.is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self._grid_z3.columns_number)] for i in range(self._grid_z3.rows_number)])
            black_shapes = current_grid.get_all_shapes()
            if len(black_shapes) == 1:
                return TapaSolver.crop_grid(current_grid), proposition_count

            biggest_shape = max(black_shapes, key=len)
            black_shapes.remove(biggest_shape)
            for black_shape in black_shapes:
                shape_not_all_black = self._solver.Not(self._solver.And([self._grid_z3[position] for position in black_shape]))
                around_shape = ShapeGenerator.around_shape(black_shape)
                around_not_all_white = self._solver.Not(self._solver.And([self._solver.Not(self._grid_z3[position]) for position in around_shape if position in self._grid_z3]))
                constraint = self._solver.Or(shape_not_all_black, around_not_all_white)
                self._solver.add(constraint)

        return Grid.empty(), proposition_count

    @staticmethod
    def crop_grid(solution_grid: Grid):
        return Grid([[True if solution_grid.value(r, c) else False for c in range(1, solution_grid.columns_number - 1)] for r in range(1, solution_grid.rows_number - 1)])

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
