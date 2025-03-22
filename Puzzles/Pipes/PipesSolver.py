from Pipes.Pipe import Pipe
from Pipes.PipeShapeTransition import PipeShapeTransition
from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Direction import Direction
from Utils.GridBase import GridBase
from Utils.PipesGrid import PipesGrid
from Utils.Position import Position

FALSE = False  # for avoid PyCharm warning


class PipesSolver(GameSolver):
    def __init__(self, grid: GridBase[Pipe], solver_engine: SolverEngine):
        self._input_grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._solver = solver_engine
        self._grid_z3: GridBase | None = None
        self._previous_solution: GridBase[Pipe] | None = None

    def _init_solver(self):
        self._grid_z3 = GridBase([
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

    def get_solution(self) -> GridBase:
        if not self._solver.has_constraints():
            self._init_solver()

        solution, _ = self.get_solution_when_all_pipes_connected()
        return solution

    def get_solution_when_all_pipes_connected(self):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            current_grid = PipesGrid([[
                self._create_pipe_from_model(model, Position(r, c))
                for c in range(self._columns_number)]
                for r in range(self._rows_number)])

            connected_positions, is_loop = current_grid.get_connected_positions_and_is_loop()
            if len(connected_positions) == 1 and not is_loop:
                self._previous_solution = current_grid
                transition_grid = GridBase([[
                    PipeShapeTransition(self._input_grid[Position(r, c)], current_grid[Position(r, c)])
                    for c in range(self._columns_number)]
                    for r in range(self._rows_number)])
                return transition_grid, proposition_count

            if len(connected_positions) > 1:
                max_connected_positions = max(connected_positions, key=len)
                connected_positions = [position for positions in connected_positions if positions != max_connected_positions for position in positions]

            constraints = []
            for position in connected_positions:
                connected_to = current_grid[position].get_connected_to()
                constraints.append(self._grid_z3[position][Direction.up()] == (Direction.up() in connected_to))
                constraints.append(self._grid_z3[position][Direction.down()] == (Direction.down() in connected_to))
                constraints.append(self._grid_z3[position][Direction.left()] == (Direction.left() in connected_to))
                constraints.append(self._grid_z3[position][Direction.right()] == (Direction.right() in connected_to))
            self._solver.add(self._solver.Not(self._solver.And(constraints)))

        return GridBase.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for position, pipe in self._previous_solution:
            connected_to = pipe.get_connected_to()
            previous_solution_constraints.append(self._grid_z3[position][Direction.up()] == (Direction.up() in connected_to))
            previous_solution_constraints.append(self._grid_z3[position][Direction.down()] == (Direction.down() in connected_to))
            previous_solution_constraints.append(self._grid_z3[position][Direction.left()] == (Direction.left() in connected_to))
            previous_solution_constraints.append(self._grid_z3[position][Direction.right()] == (Direction.right() in connected_to))

        self._solver.add(self._solver.Not(self._solver.And(previous_solution_constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_possible_rotations_constraints()
        self._add_connected_constraints()

    def _add_possible_rotations_constraints(self):
        for position, pipe_shape in self._input_grid:
            self._add_edges_constraints(position)

            match pipe_shape.shape:
                case "L":
                    self._add_shape_l_constraint(position)
                case "I":
                    self.add_shape_i_constraint(position)
                case "T":
                    self.add_shape_t_constraint(position)
                case "E":
                    self.add_shape_e_constraint(position)

    def _add_edges_constraints(self, position):
        if position.r == 0:
            self._solver.add(self._grid_z3[position][Direction.up()] == FALSE)
        if position.r == self._input_grid.rows_number - 1:
            self._solver.add(self._grid_z3[position][Direction.down()] == FALSE)
        if position.c == 0:
            self._solver.add(self._grid_z3[position][Direction.left()] == FALSE)
        if position.c == self._input_grid.columns_number - 1:
            self._solver.add(self._grid_z3[position][Direction.right()] == FALSE)

    def _add_shape_l_constraint(self, pos: Position):
        l0 = self._solver.And(self._grid_z3[pos][Direction.up()], self._grid_z3[pos][Direction.right()], self._grid_z3[pos][Direction.down()] == FALSE, self._grid_z3[pos][Direction.left()] == FALSE)
        l1 = self._solver.And(self._grid_z3[pos][Direction.left()], self._grid_z3[pos][Direction.up()], self._grid_z3[pos][Direction.right()] == FALSE, self._grid_z3[pos][Direction.down()] == FALSE)
        l2 = self._solver.And(self._grid_z3[pos][Direction.down()], self._grid_z3[pos][Direction.left()], self._grid_z3[pos][Direction.up()] == FALSE, self._grid_z3[pos][Direction.right()] == FALSE)
        l3 = self._solver.And(self._grid_z3[pos][Direction.right()], self._grid_z3[pos][Direction.down()], self._grid_z3[pos][Direction.left()] == FALSE, self._grid_z3[pos][Direction.up()] == FALSE)
        self._solver.add(self._solver.Or(l0, l1, l2, l3))

    def add_shape_i_constraint(self, position):
        i0 = self._solver.And(self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.left()] == FALSE, self._grid_z3[position][Direction.right()] == FALSE)
        i1 = self._solver.And(self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.up()] == FALSE, self._grid_z3[position][Direction.down()] == FALSE)
        self._solver.add(self._solver.Or(i0, i1))

    def add_shape_t_constraint(self, position):
        t0 = self._solver.And(self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.up()] == FALSE)
        t1 = self._solver.And(self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.left()] == FALSE)
        t2 = self._solver.And(self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.down()] == FALSE)
        t3 = self._solver.And(self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.right()] == FALSE)
        self._solver.add(self._solver.Or(t0, t1, t2, t3))

    def add_shape_e_constraint(self, position):
        e0 = self._solver.And(self._grid_z3[position][Direction.up()], self._grid_z3[position][Direction.down()] == FALSE, self._grid_z3[position][Direction.left()] == FALSE, self._grid_z3[position][Direction.right()] == FALSE)
        e1 = self._solver.And(self._grid_z3[position][Direction.left()], self._grid_z3[position][Direction.right()] == FALSE, self._grid_z3[position][Direction.up()] == FALSE, self._grid_z3[position][Direction.down()] == FALSE)
        e2 = self._solver.And(self._grid_z3[position][Direction.down()], self._grid_z3[position][Direction.up()] == FALSE, self._grid_z3[position][Direction.left()] == FALSE, self._grid_z3[position][Direction.right()] == FALSE)
        e3 = self._solver.And(self._grid_z3[position][Direction.right()], self._grid_z3[position][Direction.left()] == FALSE, self._grid_z3[position][Direction.up()] == FALSE, self._grid_z3[position][Direction.down()] == FALSE)
        self._solver.add(self._solver.Or(e0, e1, e2, e3))

    def _add_connected_constraints(self):
        for position, value in self._grid_z3:
            position_up = self._grid_z3.neighbor_up(position)
            position_down = self._grid_z3.neighbor_down(position)
            position_left = self._grid_z3.neighbor_left(position)
            position_right = self._grid_z3.neighbor_right(position)
            if position_up is not None:
                self._solver.add(self._grid_z3[position][Direction.up()] == self._grid_z3[position_up][Direction.down()])
            if position_down is not None:
                self._solver.add(self._grid_z3[position][Direction.down()] == self._grid_z3[position_down][Direction.up()])
            if position_left is not None:
                self._solver.add(self._grid_z3[position][Direction.left()] == self._grid_z3[position_left][Direction.right()])
            if position_right is not None:
                self._solver.add(self._grid_z3[position][Direction.right()] == self._grid_z3[position_right][Direction.left()])

    def _create_pipe_from_model(self, model, position: Position):
        directions = []
        if self._solver.is_true(model.eval(self._grid_z3[position][Direction.up()])):
            directions.append(Direction.up())
        if self._solver.is_true(model.eval(self._grid_z3[position][Direction.left()])):
            directions.append(Direction.left())
        if self._solver.is_true(model.eval(self._grid_z3[position][Direction.down()])):
            directions.append(Direction.down())
        if self._solver.is_true(model.eval(self._grid_z3[position][Direction.right()])):
            directions.append(Direction.right())
        return Pipe.from_connection(frozenset(directions))
