import time

from bitarray import bitarray
from z3 import Solver, sat, Or, BitVec, Extract, set_param, unsat, unknown
from Grid import Grid


class NonogramGame:
    def __init__(self, numbers_by_top_left: dict[str, list[list[int]]]):
        self._numbers_by_top_left = numbers_by_top_left
        self.rows_number = len(self._numbers_by_top_left['left'])
        self.columns_number = len(self._numbers_by_top_left['top'])
        if self.rows_number % 5 != 0:
            raise ValueError("Rows number must be divisible by 5")
        if self.columns_number % 5 != 0:
            raise ValueError("Columns number must be divisible by 5")
        if any([len(numbers) == 0 for numbers in self._numbers_by_top_left['left']]):
            raise ValueError("Missing number for row")
        if any([len(numbers) == 0 for numbers in self._numbers_by_top_left['top']]):
            raise ValueError("Missing number for column")
        self._solver = None
        self._rows_z3: list[BitVec] = []
        self._columns_z3: list[BitVec] = []

    def get_solution(self) -> Grid:
        self._rows_z3: list[BitVec] = [BitVec(f"row_{r}", self.columns_number) for r in range(self.rows_number)]
        self._columns_z3: list[BitVec] = [BitVec(f"column_{c}", self.rows_number) for c in range(self.columns_number)]
        self._solver = Solver()
        self.reset_time()
        self._init_adjacent_cells()
        self._add_constraints()
        check = self._solver.check()
        self.print_time("check solution")
        if check != sat:
            return Grid.empty()

        rows = self._compute_solution()
        return Grid(rows)

    def _compute_solution(self):
        model = self._solver.model()
        rows = []
        for i_row in range(self.rows_number):
            row_value = model[self._rows_z3[i_row]].as_long()
            row_list = [(row_value >> j) & 1 == 1 for j in range(self.columns_number - 1, -1, -1)]
            rows.append(row_list)
        return rows

    @staticmethod
    def print_time(name: str):
        return
        diff = time.time() - NonogramGame.instant_time
        NonogramGame.instant_time = time.time()
        print(f"Execution time for {name}: {diff} seconds")

    @staticmethod
    def reset_time():
        NonogramGame.instant_time = time.time()

    def _init_adjacent_cells(self):
        self.adjacent_cells_row = {cells_count: Grid.get_bit_array_adjacent_combinations(self.columns_number, cells_count, False) for cells_count in range(self.columns_number + 1)}
        self.adjacent_cells_column = {cells_count: Grid.get_bit_array_adjacent_combinations(self.rows_number, cells_count, False) for cells_count in range(self.rows_number + 1)}

    def _add_constraints(self):
        self._add_row_column_intersection_constraints()
        self._add_lines_constraints('row')
        self._add_lines_constraints('column')

    def _add_row_column_intersection_constraints(self):
        constraints_extract = []
        for i_row in range(self.rows_number):
            index_row = self.rows_number - i_row - 1
            for i_col in range(self.columns_number):
                index_col = self.columns_number - i_col - 1
                cons_extract = Extract(index_col, index_col, self._rows_z3[i_row]) == Extract(index_row, index_row, self._columns_z3[i_col])
                constraints_extract.append(cons_extract)
        self._solver.add(constraints_extract)

    def _add_lines_constraints(self, line_type: str):
        match line_type:
            case 'row':
                lines_number = self.rows_number
                other_line_number = self.columns_number
                numbers_by_line_type = self._numbers_by_top_left['left']
                lines_z3 = self._rows_z3
                other_line_type = 'column'
            case 'column':
                lines_number = self.columns_number
                other_line_number = self.rows_number
                numbers_by_line_type = self._numbers_by_top_left['top']
                lines_z3 = self._columns_z3
                other_line_type = 'row'
            case _:
                raise ValueError("Invalid line type")
        lines_constraints = []
        merged_combinations_by_numbers: dict[tuple, list] = {}
        for line_index in range(lines_number):
            trues_numbers = tuple(numbers_by_line_type[line_index])
            if any(count > self.rows_number or count < 0 for count in trues_numbers):
                raise ValueError(f"Numbers for {line_type}s must be positive and less or equal than {other_line_type}s number")
            line_z3 = lines_z3[line_index]
            if trues_numbers in merged_combinations_by_numbers:
                merged_combinations = merged_combinations_by_numbers[trues_numbers]
            else:
                merged_combinations = NonogramGame.generate_combinations(other_line_number, trues_numbers)
                merged_combinations_by_numbers[trues_numbers] = merged_combinations
            constraints = self.compute_lines_constraints(merged_combinations, line_z3)
            lines_constraints.append(constraints)
        self._solver.add(lines_constraints)

    @staticmethod
    def generate_combinations(line_length: int, blocks_lengths: tuple[int, ...]) -> list[bitarray]:
        results = []
        NonogramGame.backtrack_generate_combinations(bitarray(), 0, line_length, blocks_lengths, results)
        return results

    @staticmethod
    def backtrack_generate_combinations(current_bitarray: bitarray, block_index: int, line_length: int, blocks_lengths: tuple[int, ...], results: list[bitarray]):
        if block_index == len(blocks_lengths):
            current_bitarray.extend([0] * (line_length - len(current_bitarray)))
            if len(current_bitarray) == line_length:
                results.append(current_bitarray.copy())
            return

        block_length = blocks_lengths[block_index]
        line_index_start = len(current_bitarray)

        for line_index in range(line_index_start, line_length - block_length + 1):
            new_bitarray = current_bitarray.copy()
            new_bitarray.extend([0] * (line_index - line_index_start) + [1] * block_length)
            if block_index < len(blocks_lengths) - 1:
                new_bitarray.append(0)
            NonogramGame.backtrack_generate_combinations(new_bitarray, block_index + 1, line_length, blocks_lengths, results)

    @staticmethod
    def compute_lines_constraints(merged_combinations: list[bitarray], true_cells_line: BitVec):
        constraints = []
        for combination in merged_combinations:
            combination_int = int(combination.to01(), 2)
            constraint = true_cells_line == combination_int
            constraints.append(constraint)
        or_constraint = Or(constraints)
        return or_constraint
