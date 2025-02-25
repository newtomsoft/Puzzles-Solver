from Pipes.PipeShape import PipeShape
from Pipes.PipeShapeTransition import PipeShapeTransition
from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid
from Utils.IslandsGrid import IslandGrid
from Utils.Position import Position


class PipesSolver(GameSolver):
    def __init__(self, grid: Grid[PipeShape], solver_engine: SolverEngine):
        self._input_grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._island_grid: IslandGrid | None = None
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._last_solution: IslandGrid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([
            [
                {
                    'up': self._solver.bool(f"{r}_{c}_up"),
                    'left': self._solver.bool(f"{r}_{c}_left"),
                    'down': self._solver.bool(f"{r}_{c}_down"),
                    'right': self._solver.bool(f"{r}_{c}_right"),
                }
                for c in range(self._columns_number)
            ]
            for r in range(self._rows_number)
        ])

        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.has_constraints():
            self._init_solver()

        solution, _ = self.get_grid_when_all_pipes_connected()
        self._last_solution = solution
        return solution

    def get_grid_when_all_pipes_connected(self):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[
                PipeShape.from_connection(
                    up=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)]['up'])),
                    down=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)]['down'])),
                    left=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)]['left'])),
                    right=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)]['right']))
                )
                for c in range(self._columns_number)]
                for r in range(self._rows_number)])

            transition_grid = Grid([[
                PipeShapeTransition(self._input_grid[Position(r, c)], current_grid[Position(r, c)])
                for c in range(self._columns_number)]
                for r in range(self._rows_number)])

            return transition_grid, proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []

        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_connected_constraints()

    def _add_initial_constraints(self):
        for position, pipe_shape in self._input_grid:
            if position.r == 0:
                self._solver.add(self._grid_z3[position]['up'] == False)
            if position.r == self._input_grid.rows_number - 1:
                self._solver.add(self._grid_z3[position]['down'] == False)
            if position.c == 0:
                self._solver.add(self._grid_z3[position]['left'] == False)
            if position.c == self._input_grid.columns_number - 1:
                self._solver.add(self._grid_z3[position]['right'] == False)

            if pipe_shape.shape == "L":
                constraint_l0 = self._solver.And(self._grid_z3[position]['up'], self._grid_z3[position]['right'], self._grid_z3[position]['down'] == False, self._grid_z3[position]['left'] == False)
                constraint_l1 = self._solver.And(self._grid_z3[position]['left'], self._grid_z3[position]['up'], self._grid_z3[position]['right'] == False, self._grid_z3[position]['down'] == False)
                constraint_l2 = self._solver.And(self._grid_z3[position]['down'], self._grid_z3[position]['left'], self._grid_z3[position]['up'] == False, self._grid_z3[position]['right'] == False)
                constraint_l3 = self._solver.And(self._grid_z3[position]['right'], self._grid_z3[position]['down'], self._grid_z3[position]['left'] == False, self._grid_z3[position]['up'] == False)
                self._solver.add(self._solver.Or(constraint_l0, constraint_l1, constraint_l2, constraint_l3))
            if pipe_shape.shape == "I":
                constraint_i0 = self._solver.And(self._grid_z3[position]['up'], self._grid_z3[position]['down'], self._grid_z3[position]['left'] == False, self._grid_z3[position]['right'] == False)
                constraint_i1 = self._solver.And(self._grid_z3[position]['left'], self._grid_z3[position]['right'], self._grid_z3[position]['up'] == False, self._grid_z3[position]['down'] == False)
                self._solver.add(self._solver.Or(constraint_i0, constraint_i1))
            if pipe_shape.shape == "T":
                constraint_t0 = self._solver.And(self._grid_z3[position]['down'], self._grid_z3[position]['left'], self._grid_z3[position]['right'], self._grid_z3[position]['up'] == False)
                constraint_t1 = self._solver.And(self._grid_z3[position]['right'], self._grid_z3[position]['up'], self._grid_z3[position]['down'], self._grid_z3[position]['left'] == False)
                constraint_t2 = self._solver.And(self._grid_z3[position]['up'], self._grid_z3[position]['right'], self._grid_z3[position]['left'], self._grid_z3[position]['down'] == False)
                constraint_t3 = self._solver.And(self._grid_z3[position]['left'], self._grid_z3[position]['down'], self._grid_z3[position]['up'], self._grid_z3[position]['right'] == False)
                self._solver.add(self._solver.Or(constraint_t0, constraint_t1, constraint_t2, constraint_t3))
            if pipe_shape.shape == "E":
                constraint_e0 = self._solver.And(
                    self._grid_z3[position]['up'], self._grid_z3[position]['down'] == False, self._grid_z3[position]['left'] == False, self._grid_z3[position]['right'] == False)
                constraint_e1 = self._solver.And(
                    self._grid_z3[position]['left'], self._grid_z3[position]['right'] == False, self._grid_z3[position]['up'] == False, self._grid_z3[position]['down'] == False)
                constraint_e2 = self._solver.And(
                    self._grid_z3[position]['down'], self._grid_z3[position]['up'] == False, self._grid_z3[position]['left'] == False, self._grid_z3[position]['right'] == False)
                constraint_e3 = self._solver.And(
                    self._grid_z3[position]['right'], self._grid_z3[position]['left'] == False, self._grid_z3[position]['up'] == False, self._grid_z3[position]['down'] == False)
                self._solver.add(self._solver.Or(constraint_e0, constraint_e1, constraint_e2, constraint_e3))

    def _add_connected_constraints(self):
        for position, value in self._grid_z3:
            position_up = self._grid_z3.neighbor_position_up(position)
            position_down = self._grid_z3.neighbor_position_down(position)
            position_left = self._grid_z3.neighbor_position_left(position)
            position_right = self._grid_z3.neighbor_position_right(position)
            if position_up is not None:
                self._solver.add(self._grid_z3[position]['up'] == self._grid_z3[position_up]['down'])
            if position_down is not None:
                self._solver.add(self._grid_z3[position]['down'] == self._grid_z3[position_down]['up'])
            if position_left is not None:
                self._solver.add(self._grid_z3[position]['left'] == self._grid_z3[position_left]['right'])
            if position_right is not None:
                self._solver.add(self._grid_z3[position]['right'] == self._grid_z3[position_right]['left'])
