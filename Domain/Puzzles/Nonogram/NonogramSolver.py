from ortools.sat.python.cp_model import CpModel, CpSolver, OPTIMAL, FEASIBLE
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

        self._model = CpModel()
        self._solver = CpSolver()
        self._grid_ortools: list[list] = []
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        if not self._grid_ortools:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (OPTIMAL, FEASIBLE):
            return Grid.empty()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        literals = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._previous_solution.value(r, c) == 1:
                    literals.append(self._grid_ortools[r][c].Not())
                else:
                    literals.append(self._grid_ortools[r][c])
        self._model.add_bool_or(literals)

        status = self._solver.solve(self._model)
        if status not in (OPTIMAL, FEASIBLE):
            return Grid.empty()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _init_solver(self):
        self._grid_ortools = [[self._model.new_bool_var(f"cell_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()

    def _compute_solution(self):
        solution = []
        for r in range(self.rows_number):
            row_list = [int(self._solver.boolean_value(self._grid_ortools[r][c])) for c in range(self.columns_number)]
            solution.append(row_list)
        return Grid(solution)

    def _add_constraints(self):
        self._add_lines_constraints('row')
        self._add_lines_constraints('column')

    def _add_lines_constraints(self, line_type: str):
        match line_type:
            case 'row':
                lines_number = self.rows_number
                other_line_number = self.columns_number
                numbers_by_line_type = self._numbers_left
                other_line_type = 'column'
            case 'column':
                lines_number = self.columns_number
                other_line_number = self.rows_number
                numbers_by_line_type = self._numbers_top
                other_line_type = 'row'
            case _:
                raise ValueError("Invalid line type")

        for line_index in range(lines_number):
            numbers = tuple(numbers_by_line_type[line_index])
            if any(count > other_line_number or count < 0 for count in numbers):
                raise ValueError(f"Numbers for {line_type}s must be positive and less or equal than {other_line_type}s number")

            if line_type == 'row':
                line_vars = self._grid_ortools[line_index]
            else:
                line_vars = [self._grid_ortools[r][line_index] for r in range(self.rows_number)]

            self._add_automaton_constraint(line_vars, numbers)

    def _add_automaton_constraint(self, line_vars, blocks):
        blocks = [b for b in blocks if b > 0]
        transitions = [(0, 0, 0)]

        if not blocks:
            self._model.add_automaton(line_vars, 0, [0], transitions)
            return

        current_state = 0
        for i, length in enumerate(blocks):
            start_block_state = current_state
            next_state = current_state + 1
            transitions.append((start_block_state, 1, next_state))

            for _ in range(length - 1):
                transitions.append((next_state, 1, next_state + 1))
                next_state += 1
            
            if i < len(blocks) - 1:
                gap_state = next_state + 1
                transitions.append((next_state, 0, gap_state))
                transitions.append((gap_state, 0, gap_state))
                current_state = gap_state
            else:
                end_state = next_state + 1
                transitions.append((next_state, 0, end_state))
                transitions.append((end_state, 0, end_state))
                current_state = end_state

        accept_states = [current_state, current_state - 1]

        self._model.add_automaton(line_vars, 0, accept_states, transitions)
