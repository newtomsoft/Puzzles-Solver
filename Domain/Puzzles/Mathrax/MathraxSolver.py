from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver

class MathraxSolver(GameSolver):
    def __init__(self, grid: Grid, constraints: list[dict[str, int | tuple[int, int]]]):
        self.grid = grid
        self.size = grid.rows_number
        self.constraints = constraints # list of dict: {'pos': (r, c), 'op': '+', 'val': 10} or {'op': 'E'} etc.
        self._model = cp_model.CpModel()
        self._vars = [[self._model.new_int_var(1, self.size, f'cell_{r}_{c}') for c in range(self.size)] for r in range(self.size)]
        
        for r in range(self.size):
            for c in range(self.size):
                val = self.grid.value(r, c)
                if val != 0:
                    self._model.add(self._vars[r][c] == val)
        
        self._add_constraints()

    def _add_constraints(self):
        for r in range(self.size):
            self._model.add_all_different(self._vars[r])
        for c in range(self.size):
            self._model.add_all_different([self._vars[r][c] for r in range(self.size)])

        for constraint in self.constraints:
            r, c = constraint['pos']
            cells = [self._vars[r][c], self._vars[r][c+1], self._vars[r+1][c], self._vars[r+1][c+1]]
            op = constraint['op']
            val = constraint.get('val')

            if op == '+':
                if val > (2 * self.size - 1):
                    self._model.add(sum(cells) == val)
                else:
                    self._model.add(cells[0] + cells[3] == val)
                    self._model.add(cells[1] + cells[2] == val)
            elif op == '-':
                # Diagonals
                diff1 = self._model.new_int_var(0, self.size, f'diff1_{r}_{c}')
                diff2 = self._model.new_int_var(0, self.size, f'diff2_{r}_{c}')
                self._model.add_abs_equality(diff1, cells[0] - cells[3])
                self._model.add_abs_equality(diff2, cells[1] - cells[2])
                self._model.add(diff1 == val)
                self._model.add(diff2 == val)
            elif op == '*':
                for (a, b) in [(cells[0], cells[3]), (cells[1], cells[2])]:
                    self._model.add_multiplication_equality(val, [a, b])
            elif op == '/':
                for (a, b) in [(cells[0], cells[3]), (cells[1], cells[2])]:
                    b1 = self._model.new_bool_var(f'ratio_b1_{r}_{c}_{a}_{b}')
                    b2 = self._model.new_bool_var(f'ratio_b2_{r}_{c}_{a}_{b}')
                    self._model.add(a == val * b).only_enforce_if(b1)
                    self._model.add(b == val * a).only_enforce_if(b2)
                    self._model.add(b1 + b2 == 1)
            elif op == 'E':
                for cell in cells:
                    self._model.add_modulo_equality(0, cell, 2)
            elif op == 'O':
                for cell in cells:
                    self._model.add_modulo_equality(1, cell, 2)

    def get_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            matrix = [[solver.value(self._vars[r][c]) for c in range(self.size)] for r in range(self.size)]
            self._last_solution_matrix = matrix
            return Grid(matrix)
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if not hasattr(self, '_last_solution_matrix'):
            self.get_solution()
        
        if not hasattr(self, '_last_solution_matrix'):
            return Grid.empty()

        literals = []
        for r in range(self.size):
            for c in range(self.size):
                diff_var = self._model.new_bool_var(f'diff_{r}_{c}')
                self._model.add(self._vars[r][c] != self._last_solution_matrix[r][c]).only_enforce_if(diff_var)
                literals.append(diff_var)
        
        self._model.add(sum(literals) >= 1)
        
        solver = cp_model.CpSolver()
        status = solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            matrix = [[solver.value(self._vars[r][c]) for c in range(self.size)] for r in range(self.size)]
            return Grid(matrix)
        return Grid.empty()
