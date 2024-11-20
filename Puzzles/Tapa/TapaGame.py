from z3 import Bool, Solver, Implies, Not, And, Or, sat, is_true, Sum

from Puzzles.Tapa.ShapeCollection import ShapeCollection
from Puzzles.Tapa.ShapeGenerator import ShapeGenerator
from Utils.Grid import Grid


class TapaGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 2 or self.columns_number < 2:
            raise ValueError("The grid must be at least 2x2")
        if not any(isinstance(cell, list) for row in self._grid.matrix for cell in row):
            raise ValueError("The grid must contain at least one list number")
        self._solver = None
        self._grid_z3 = None
        self.min_black = self._get_min_black()

    def get_solution(self) -> (Grid | None, int):
        matrix_z3 = [[Bool(f"bool_{r}_{c}") for c in range(1 + self._grid.columns_number + 1)] for r in range(1 + self._grid.rows_number + 1)]
        #  True for black, False for white
        self._grid_z3 = Grid(matrix_z3)
        self._solver = Solver()

        self._init_borders_white()
        self._init_adjacent_cells()
        self._min_black()
        self._max_black()
        self._no_black_on_numbers_cell()
        self._black_around_number()
        self._no_black_square()
        self._no_isolated_black_shape()

        solution, propositions_count = self._ensure_all_black_connected()
        return solution, propositions_count

    def _init_borders_white(self):
        self._solver.add([Not(self._grid_z3.value(r, 0)) for r in range(self._grid_z3.rows_number)])
        self._solver.add([Not(self._grid_z3.value(r, self._grid_z3.columns_number - 1)) for r in range(self._grid_z3.rows_number)])
        self._solver.add([Not(self._grid_z3.value(0, c)) for c in range(self._grid_z3.columns_number)])
        self._solver.add([Not(self._grid_z3.value(self._grid_z3.rows_number - 1, c)) for c in range(self._grid_z3.columns_number)])

    def _min_black(self):
        self._solver.add(Sum([self._grid_z3.value(r, c) for r in range(1, self._grid_z3.rows_number - 1) for c in range(1, self._grid_z3.columns_number - 1)]) >= self.min_black)

    def _max_black(self):
        max_black = self.rows_number * self.columns_number - (self.rows_number // 2) * (self.columns_number // 2)
        self._solver.add(Sum([self._grid_z3.value(r, c) for r in range(1, self._grid_z3.rows_number - 1) for c in range(1, self._grid_z3.columns_number - 1)]) <= max_black)

    def _no_black_on_numbers_cell(self):
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if isinstance(self._grid.value(r, c), list):
                    self._solver.add(Not(self._grid_z3.value(r + 1, c + 1)))

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
                merged_combinations = TapaGame._combine_list_with_gap(adjacent_combinations)
                constraints = []
                for combination in merged_combinations:
                    constraints.append(And([black_cells_around[i] if combination[i] else Not(black_cells_around[i]) for i in range(len(combination))]))
                self._solver.add(Or(constraints))

    def _no_black_square(self):
        for c in range(1, self._grid_z3.columns_number - 1):
            for r in range(1, self._grid_z3.rows_number - 1):
                self._solver.add(Or(
                    Not(self._grid_z3.value(r, c)),
                    Not(self._grid_z3.value(r + 1, c)),
                    Not(self._grid_z3.value(r, c + 1)),
                    Not(self._grid_z3.value(r + 1, c + 1))
                ))

    def _no_isolated_black_shape(self):
        max_size = min(self.min_black, int(min(self._grid.columns_number, self._grid.rows_number) / 2))
        shapes_and_outlines = []
        for current_max_size in range(1, max_size + 1):
            shapes_and_outlines += ShapeCollection.get_shapes_arounds_by_size((1, current_max_size))

        for shape_and_outline in shapes_and_outlines:
            shape = shape_and_outline[0]
            outline = shape_and_outline[1]
            shape_rows_number = max([r for r, c in shape]) + 1
            shape_columns_number = max([c for r, c in shape]) + 1
            if shape_rows_number >= self._grid.rows_number - 1 or shape_columns_number >= self._grid.columns_number - 1:
                continue
            constraints = []
            for r in range(1, self._grid_z3.rows_number - shape_rows_number):
                for c in range(1, self._grid_z3.columns_number - shape_columns_number):
                    if isinstance(self._grid.value(r - 1, c - 1), list):
                        continue
                    are_numbers = any([isinstance(self._grid.value(r + dr - 1, c + dc - 1), list) for dr, dc in shape])
                    if are_numbers:
                        continue
                    shape_black = And([self._grid_z3.value(r + dr, c + dc) for dr, dc in shape])
                    around_all_white = And([Not(self._grid_z3.value(r + dr, c + dc)) for dr, dc in outline])
                    around_not_all_white = Not(around_all_white)
                    constraints.append(Implies(shape_black, around_not_all_white))
            self._solver.add(constraints)

    def _ensure_all_black_connected(self) -> (Grid | None, int):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self._grid_z3.columns_number)] for i in range(self._grid_z3.rows_number)])
            is_solution = current_grid.are_all_cells_connected()
            if is_solution:
                return TapaGame.crop_grid(current_grid), proposition_count

            black_shapes = current_grid.get_all_shapes(True)
            biggest_shape = max(black_shapes, key=len)
            black_shapes.remove(biggest_shape)
            for black_shape in black_shapes:
                shape_not_all_black = Not(And([self._grid_z3.value(r, c) for r, c in black_shape]))
                around_shape = ShapeGenerator.around_shape(black_shape)
                around_not_all_white = Not(And([Not(self._grid_z3.value(r, c)) for r, c in around_shape]))
                constraint = Or(shape_not_all_black, around_not_all_white)
                self._solver.add(constraint)

        return None, proposition_count

    @staticmethod
    def crop_grid(solution_grid: Grid):
        return Grid([[True if solution_grid.value(r, c) else False for c in range(1, solution_grid.columns_number - 1)] for r in range(1, solution_grid.rows_number - 1)])

    def _init_adjacent_cells(self):
        neighbors_count = 8
        self.adjacent_cells = {cells_count: Grid.get_adjacent_combinations(neighbors_count, cells_count, True) for cells_count in range(neighbors_count + 1)}

    @staticmethod
    def _combine_with_gap(blocks1: list[list[bool]], blocks2: list[list[bool]]) -> list[list[bool]]:
        true_count = blocks1[0].count(True) + blocks2[0].count(True)
        block_count = TapaGame._adjacent_group_count(blocks1[0]) + TapaGame._adjacent_group_count(blocks2[0])
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
                if TapaGame._adjacent_group_count(combined) == block_count:
                    result.append(combined)
        return result

    @staticmethod
    def _combine_list_with_gap(blocks_list: list[list[list[bool]]]) -> list[list[bool]]:
        if len(blocks_list) == 1:
            return blocks_list[0]
        if len(blocks_list) == 2:
            return TapaGame._combine_with_gap(blocks_list[0], blocks_list[1])
        result = TapaGame._combine_list_with_gap([TapaGame._combine_with_gap(blocks_list[0], blocks_list[1])] + blocks_list[2:])
        return result

    @staticmethod
    def _adjacent_group_count(combination: list[bool]):
        return combination.count(True) - TapaGame._adjacent_count(combination)

    @staticmethod
    def _adjacent_count(block: list[bool]):
        return sum(block[i] and block[i + 1] for i in range(len(block) - 1)) + (block[0] and block[-1])

    def get_console_grid(self, solution_grid):
        background_grid = Grid([[1 if solution_grid.value(r, c) else 0 for c in range(solution_grid.columns_number)] for r in range(solution_grid.rows_number)])
        numbers_grid = Grid([[TapaGame.list_to_string(self._grid.value(r, c)) if isinstance(self._grid.value(r, c), list) else ' ' for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        police_color_grid = Grid([[16 for _ in range(solution_grid.columns_number)] for _ in range(solution_grid.rows_number)])
        console_grid = numbers_grid.to_console_string(police_color_grid, background_grid)
        return console_grid

    @staticmethod
    def list_to_string(array):
        return sum(array)

    def _get_min_black(self):
        number_sum = 0
        for r in range(0, self._grid.rows_number, 5):
            for c in range(0, self._grid.columns_number, 5):
                max_number = 0
                for dr in range(min(5, self._grid.rows_number - r)):
                    for dc in range(min(5, self._grid.columns_number - c)):
                        number = sum(self._grid.value(r + dr, c + dc)) if isinstance(self._grid.value(r + dr, c + dc), list) else 0
                        if number > max_number:
                            max_number = number
                number_sum += max_number
        return number_sum
