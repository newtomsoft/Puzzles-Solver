from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class CreekSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.solution_rows_number = self._grid.rows_number - 1
        self.solution_columns_number = self._grid.columns_number - 1
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[self._solver.bool(f"grid_{r}_{c}") for c in range(self.solution_columns_number)] for r in range(self.solution_rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.has_constraints():
            self._init_solver()

        solution, _ = self._ensure_all_river_connected()
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        previous_solution_constraints = []
        for position, _ in [(position, value) for (position, value) in self._previous_solution if not value]:
            previous_solution_constraints.append(self._solver.Not(self._grid_z3[position]))
        self._solver.add(self._solver.Not(self._solver.And(previous_solution_constraints)))

        return self.get_solution()

    def _ensure_all_river_connected(self):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[self._solver.is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self.solution_columns_number)] for i in range(self.solution_rows_number)])
            river_shapes = current_grid.get_all_shapes(value=False)
            if len(river_shapes) == 1:
                return current_grid, proposition_count

            biggest_river_shapes = max(river_shapes, key=len)
            river_shapes.remove(biggest_river_shapes)
            for river_shape in river_shapes:
                in_all_river = self._solver.And([self._solver.Not(self._grid_z3[position]) for position in river_shape])
                around_all_forest = self._solver.And([self._grid_z3[position] for position in ShapeGenerator.around_shape(river_shape) if position in self._grid_z3])
                constraint = self._solver.Not(self._solver.And(around_all_forest, in_all_river))
                self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def _add_constraints(self):
        self._add_neighbors_count_constraints()

    def _add_neighbors_count_constraints(self):
        for position, creek_count in [(position, value) for position, value in self._grid if value != -1]:
            solution_positions = self._get_positions_in_solution_grid(self._grid_z3, position)
            self._solver.add(self._solver.sum([self._grid_z3[solution_position] for solution_position in solution_positions]) == creek_count)

    @staticmethod
    def _get_positions_in_solution_grid(grid: Grid, position: Position) -> set[Position]:
        return {neighbor for neighbor in grid.straddled_neighbors_positions(Position(position.r - 0.5, position.c - 0.5))}
