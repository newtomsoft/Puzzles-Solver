from z3 import Solver, Not, And, unsat, Or, Int, Distinct, Implies

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class GyokusekiSolver(GameSolver):
    def __init__(self, counts: dict[str, list[int]]):
        self._counts_by_edge: dict[str, list[int]] = counts
        self.rows_number = len(self._counts_by_edge['up'])
        self.columns_number = len(self._counts_by_edge['left'])
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution_grid = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"cell{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._grid_z3[Position(r, c)]).as_long() for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution_grid = grid
        return grid

    def get_other_solution(self):
        exclusion_constraint = Not(
            And([self._grid_z3[Position(r, c)] == self._previous_solution_grid[Position(r, c)] for r in range(self.rows_number) for c in
                 range(self.columns_number) if self._previous_solution_grid.value(r, c)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_blacks_constraints()
        self._add_whites_constraints()

    def _add_initial_constraints(self):
        for _, value in self._grid_z3:
            self._solver.add(Or(value == 0, value == 1, value == 2))

    def _add_blacks_constraints(self):
        for r in range(self.rows_number):
                self._solver.add(sum([self._grid_z3[Position(r, c)] == 2 for c in range(self.columns_number)]) == 1)

        for c in range(self.columns_number):
                self._solver.add(sum([self._grid_z3[Position(r, c)] == 2 for r in range(self.rows_number)]) == 1)

    def _add_whites_constraints(self):
        for edge, counts_line in self._counts_by_edge.items():
            match edge:
                case 'up':
                    for index, c in enumerate(range(self.columns_number)):
                        positions = [self._grid_z3[Position(r, c)] for r in range(self.rows_number)]
                        self._add_segment_whites_constraints(counts_line[index], positions)
                case 'down':
                    for index, c in enumerate(range(self.columns_number)):
                        positions = [self._grid_z3[Position(r, c)] for r in range(self.rows_number - 1, -1, -1)]
                        self._add_segment_whites_constraints(counts_line[index], positions)
                case 'left':
                    for index, r in enumerate(range(self.rows_number)):
                        positions = [self._grid_z3[Position(r, c)] for c in range(self.columns_number)]
                        self._add_segment_whites_constraints(counts_line[index], positions)
                case 'right':
                    for index, r in enumerate(range(self.rows_number)):
                        positions = [self._grid_z3[Position(r, c)] for c in range(self.columns_number - 1, -1, -1)]
                        self._add_segment_whites_constraints(counts_line[index], positions)


    def _add_segment_whites_constraints(self, count: int, values_z3: list):
        if count == -1:
            return

        whites_count = count -1
        for black_index in range(whites_count):
            self._solver.add(values_z3[black_index] != 2)
        for black_index in range(whites_count, len(values_z3)):
            constraint_whites = sum([values_z3[index] == 1 for index in range(black_index)]) == whites_count
            self._solver.add(Implies(values_z3[black_index] == 2, constraint_whites))


