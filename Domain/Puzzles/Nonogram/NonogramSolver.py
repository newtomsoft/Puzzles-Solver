from bitarray import bitarray
from z3 import BitVec, Extract, Or, Solver, sat

from Domain.Board.Grid import Grid


class NonogramSolver:
    def __init__(self, numbers_by_top_left: dict[str, list[list[int]]]):
        self._numbers_left = numbers_by_top_left['left']
        self._numbers_top = numbers_by_top_left['top']
        self.rows_number = len(self._numbers_left)
        self.columns_number = len(self._numbers_top)
        if self.rows_number % 5 != 0:
            raise ValueError("Rows number must be divisible by 5")
        if self.columns_number % 5 != 0:
            raise ValueError("Columns number must be divisible by 5")
        if any([len(numbers) == 0 for numbers in self._numbers_left]):
            raise ValueError("Missing number for row")
        if any([len(numbers) == 0 for numbers in self._numbers_top]):
            raise ValueError("Missing number for column")
        self._solver = None
        self._rows_z3: list = []
        self._columns_z3: list = []

    def get_solution(self) -> Grid:
        self._rows_z3: list = [BitVec(f"row_{r}", self.columns_number) for r in range(self.rows_number)]
        self._columns_z3: list = [BitVec(f"column_{c}", self.rows_number) for c in range(self.columns_number)]
        self._solver = Solver()
        self._add_constraints()
        if self._solver.check() != sat:
            return Grid.empty()

        return self._compute_solution()

    def _compute_solution(self):
        model = self._solver.model()
        solution = []
        for i_row in range(self.rows_number):
            row_value = model[self._rows_z3[i_row]].as_long()
            row_list = [(row_value >> j) & 1 for j in range(self.columns_number - 1, -1, -1)]
            solution.append(row_list)
        return Grid(solution)

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
                numbers_by_line_type = self._numbers_left
                lines_z3 = self._rows_z3
                other_line_type = 'column'
            case 'column':
                lines_number = self.columns_number
                other_line_number = self.rows_number
                numbers_by_line_type = self._numbers_top
                lines_z3 = self._columns_z3
                other_line_type = 'row'
            case _:
                raise ValueError("Invalid line type")
        combinations_by_numbers: dict[tuple, list] = {}
        for line_index in range(lines_number):
            numbers = tuple(numbers_by_line_type[line_index])
            if any(count > self.rows_number or count < 0 for count in numbers):
                raise ValueError(f"Numbers for {line_type}s must be positive and less or equal than {other_line_type}s number")
            line_z3 = lines_z3[line_index]
            if numbers in combinations_by_numbers:
                combinations = combinations_by_numbers[numbers]
            else:
                combinations = NonogramSolver.generate_combinations(other_line_number, numbers)
                combinations_by_numbers[numbers] = combinations
            constraint = self.compute_line_constraint(combinations, line_z3)
            self._solver.add(constraint)

    @staticmethod
    def generate_combinations(line_length: int, blocks_lengths: tuple[int, ...]) -> list[bitarray]:
        combinations = []
        NonogramSolver.backtrack_generate_combinations(bitarray(), 0, line_length, blocks_lengths, combinations)
        return combinations

    @staticmethod
    def backtrack_generate_combinations(current_bitarray: bitarray, block_index: int, line_length: int, blocks_lengths: tuple[int, ...], combinations: list[bitarray]):
        if block_index == len(blocks_lengths):
            current_bitarray.extend([0] * (line_length - len(current_bitarray)))
            if len(current_bitarray) == line_length:
                combinations.append(current_bitarray.copy())
            return

        block_length = blocks_lengths[block_index]
        line_index_start = len(current_bitarray)

        for line_index in range(line_index_start, line_length - block_length + 1):
            new_bitarray = current_bitarray.copy()
            new_bitarray.extend([0] * (line_index - line_index_start) + [1] * block_length)
            if block_index < len(blocks_lengths) - 1:
                new_bitarray.append(0)
            NonogramSolver.backtrack_generate_combinations(new_bitarray, block_index + 1, line_length, blocks_lengths, combinations)

    @staticmethod
    def compute_line_constraint(combinations: list[bitarray], line_z3: BitVec):
        constraints = []
        for combination in combinations:
            combination_int = int(combination.to01(), 2)
            constraint = line_z3 == combination_int
            constraints.append(constraint)
        return Or(constraints)
