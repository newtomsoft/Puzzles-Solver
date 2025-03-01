from Pipes.Pipe import Pipe
from Pipes.PipeShapeTransition import PipeShapeTransition
from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.PipesGrid import PipesGrid
from Utils.Position import Position


class PipesSolver(GameSolver):
    def __init__(self, grid: Grid[Pipe], solver_engine: SolverEngine):
        self._input_grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._last_solution: Grid[Pipe] | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([
            [
                {
                    Direction.up(): self._solver.bool(f"{r}_{c}_up"),
                    Direction.left(): self._solver.bool(f"{r}_{c}_left"),
                    Direction.down(): self._solver.bool(f"{r}_{c}_down"),
                    Direction.right(): self._solver.bool(f"{r}_{c}_right"),
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

        return solution

    def get_grid_when_all_pipes_connected(self):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            current_grid = PipesGrid([[
                Pipe.from_connection(
                    up=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)][Direction.up()])),
                    down=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)][Direction.down()])),
                    left=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)][Direction.left()])),
                    right=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)][Direction.right()]))
                )
                for c in range(self._columns_number)]
                for r in range(self._rows_number)])

            connected_positions, is_loop = current_grid.get_connected_positions_and_is_loop()
            if len(connected_positions) == 1 and not is_loop:
                self._last_solution = current_grid
                transition_grid = Grid([[
                    PipeShapeTransition(self._input_grid[Position(r, c)], current_grid[Position(r, c)])
                    for c in range(self._columns_number)]
                    for r in range(self._rows_number)])
                return transition_grid, proposition_count

            if len(connected_positions) > 1:
                max_connected_positions = max(connected_positions, key=len)
                connected_positions = [position for positions in connected_positions if positions != max_connected_positions for position in positions]

            constraints = []
            for position in connected_positions:
                open_to = current_grid[position].get_open_to()
                constraints.append(self._grid_z3[position][Direction.up()] == open_to[Direction.up()])
                constraints.append(self._grid_z3[position][Direction.down()] == open_to[Direction.down()])
                constraints.append(self._grid_z3[position][Direction.left()] == open_to[Direction.left()])
                constraints.append(self._grid_z3[position][Direction.right()] == open_to[Direction.right()])
            self._solver.add(self._solver.Not(self._solver.And(constraints)))

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for position, pipe in self._last_solution:
            open_to = pipe.get_open_to()
            previous_solution_constraints.append(self._grid_z3[position][Direction.up()] == open_to[Direction.up()])
            previous_solution_constraints.append(self._grid_z3[position][Direction.down()] == open_to[Direction.down()])
            previous_solution_constraints.append(self._grid_z3[position][Direction.left()] == open_to[Direction.left()])
            previous_solution_constraints.append(self._grid_z3[position][Direction.right()] == open_to[Direction.right()])

        self._solver.add(self._solver.Not(self._solver.And(previous_solution_constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_connected_constraints()

    def _add_initial_constraints(self):
        false = False
        for position, pipe_shape in self._input_grid:
            if position.r == 0:
                self._solver.add(self._grid_z3[position][Direction.up()] == false)
            if position.r == self._input_grid.rows_number - 1:
                self._solver.add(self._grid_z3[position][Direction.down()] == false)
            if position.c == 0:
                self._solver.add(self._grid_z3[position][Direction.left()] == false)
            if position.c == self._input_grid.columns_number - 1:
                self._solver.add(self._grid_z3[position][Direction.right()] == false)

            if pipe_shape.shape == "L":
                constraint_l0 = self._solver.And(self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.down()] == false,
                                                 self._grid_z3[position][Direction.left()] == false)
                constraint_l1 = self._solver.And(self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.right()] == false,
                                                 self._grid_z3[position][Direction.down()] == false)
                constraint_l2 = self._solver.And(self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.up()] == false,
                                                 self._grid_z3[position][Direction.right()] == false)
                constraint_l3 = self._solver.And(self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.left()] == false,
                                                 self._grid_z3[position][Direction.up()] == false)
                self._solver.add(self._solver.Or(constraint_l0, constraint_l1, constraint_l2, constraint_l3))
            if pipe_shape.shape == "I":
                constraint_i0 = self._solver.And(self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.left()] == false,
                                                 self._grid_z3[position][Direction.right()] == false)
                constraint_i1 = self._solver.And(self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.up()] == false,
                                                 self._grid_z3[position][Direction.down()] == false)
                self._solver.add(self._solver.Or(constraint_i0, constraint_i1))
            if pipe_shape.shape == "T":
                constraint_t0 = self._solver.And(self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.right()],
                                                 self._grid_z3[position][Direction.up()] == false)
                constraint_t1 = self._solver.And(self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.down()],
                                                 self._grid_z3[position][Direction.left()] == false)
                constraint_t2 = self._solver.And(self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.left()],
                                                 self._grid_z3[position][Direction.down()] == false)
                constraint_t3 = self._solver.And(self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.up()],
                                                 self._grid_z3[position][Direction.right()] == false)
                self._solver.add(self._solver.Or(constraint_t0, constraint_t1, constraint_t2, constraint_t3))
            if pipe_shape.shape == "E":
                constraint_e0 = self._solver.And(
                    self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.down()] == false, self._grid_z3[position][Direction.left()] == false,
                                                             self._grid_z3[position][Direction.right()] == false)
                constraint_e1 = self._solver.And(
                    self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.right()] == false, self._grid_z3[position][Direction.up()] == false,
                                                               self._grid_z3[position][Direction.down()] == false)
                constraint_e2 = self._solver.And(
                    self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.up()] == false, self._grid_z3[position][Direction.left()] == false,
                                                               self._grid_z3[position][Direction.right()] == false)
                constraint_e3 = self._solver.And(
                    self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.left()] == false, self._grid_z3[position][Direction.up()] == false,
                                                                self._grid_z3[position][Direction.down()] == false)
                self._solver.add(self._solver.Or(constraint_e0, constraint_e1, constraint_e2, constraint_e3))

    def _add_connected_constraints(self):
        for position, value in self._grid_z3:
            position_up = self._grid_z3.neighbor_position_up(position)
            position_down = self._grid_z3.neighbor_position_down(position)
            position_left = self._grid_z3.neighbor_position_left(position)
            position_right = self._grid_z3.neighbor_position_right(position)
            if position_up is not None:
                self._solver.add(self._grid_z3[position][Direction.up()] == self._grid_z3[position_up][Direction.down()])
            if position_down is not None:
                self._solver.add(self._grid_z3[position][Direction.down()] == self._grid_z3[position_down][Direction.up()])
            if position_left is not None:
                self._solver.add(self._grid_z3[position][Direction.left()] == self._grid_z3[position_left][Direction.right()])
            if position_right is not None:
                self._solver.add(self._grid_z3[position][Direction.right()] == self._grid_z3[position_right][Direction.left()])
