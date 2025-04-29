from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver


class CreeksSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.solution_rows_number = self._grid.rows_number - 1
        self.solution_columns_number = self._grid.columns_number - 1
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> (Grid, int):
        self._grid_z3 = Grid([[self._solver.bool(f"grid_{r}_{c}") for c in range(self.solution_columns_number)] for r in range(self.solution_rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if not self._solver.has_solution():
            return Grid.empty()
        return Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_sum_neighbors_constraints()

    def _add_sum_neighbors_constraints(self):
        for position in self._grid.edges_positions():
            if position.r == 0 and position.c == 0:
                pass


    def map_position(self, grid: Grid, position: Position) -> set[Position]:
        if position.r == 0 and position.c == 0:
            return {position}
        elif position.r == self.rows_number - 1 and position.c == self.columns_number - 1:
            return {position.up_left}
        elif position.r == self.rows_number - 1:
            return {position.up}
        elif position.c == self.columns_number - 1:
            return {position.left}
        else:
            return {neighbor for neighbor in grid.straddled_neighbors_positions(Position(position.r-0.5, position.c -0.5))}


