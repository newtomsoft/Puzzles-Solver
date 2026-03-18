from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.GridBase import GridBase
from Domain.Board.Pipe import Pipe
from Domain.Board.PipesGrid import PipesGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Domain.Puzzles.Pipes.PipeShapeTransition import PipeShapeTransition


class PipesSolver(GameSolver):
    def __init__(self, grid: GridBase[Pipe]):
        self._input_grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars: GridBase | None = None
        self._previous_solution: GridBase[Pipe] | None = None

    def _init_solver(self):
        self._grid_vars = GridBase(
            [
                [
                    {
                        Direction.up(): self._model.new_bool_var(f"{r}_{c}_up"),
                        Direction.left(): self._model.new_bool_var(f"{r}_{c}_left"),
                        Direction.down(): self._model.new_bool_var(f"{r}_{c}_down"),
                        Direction.right(): self._model.new_bool_var(f"{r}_{c}_right"),
                    }
                    for c in range(self._columns_number)
                ]
                for r in range(self._rows_number)
            ]
        )

        self._add_constraints()

    def get_solution(self) -> GridBase:
        if self._grid_vars is None:
            self._init_solver()

        solution, _ = self.get_solution_when_all_pipes_connected()
        return solution

    def get_solution_when_all_pipes_connected(self):
        proposition_count = 0
        status = self._solver.solve(self._model)

        while status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            proposition_count += 1
            current_grid = PipesGrid([[self._create_pipe_from_model(Position(r, c)) for c in range(self._columns_number)] for r in range(self._rows_number)])

            connected_positions, is_loop = current_grid.get_connected_positions_and_is_loop()
            if len(connected_positions) == 1 and not is_loop:
                self._previous_solution = current_grid
                transition_grid = GridBase(
                    [[PipeShapeTransition(self._input_grid[Position(r, c)], current_grid[Position(r, c)]) for c in range(self._columns_number)] for r in range(self._rows_number)]
                )
                return transition_grid, proposition_count

            if len(connected_positions) > 1:
                max_connected_positions = max(connected_positions, key=len)
                connected_positions = [position for positions in connected_positions if positions != max_connected_positions for position in positions]

            # Add constraints to exclude this solution
            exclusion_literals = []
            for position in connected_positions:
                connected_to = current_grid[position].get_connected_to()
                for direction, is_connected in [
                    (Direction.up(), Direction.up() in connected_to),
                    (Direction.down(), Direction.down() in connected_to),
                    (Direction.left(), Direction.left() in connected_to),
                    (Direction.right(), Direction.right() in connected_to),
                ]:
                    temp_var = self._model.new_bool_var(f"excl_{position}_{direction}")
                    self._model.add(self._grid_vars[position][direction] == is_connected).only_enforce_if(temp_var)
                    self._model.add(self._grid_vars[position][direction] != is_connected).only_enforce_if(temp_var.Not())
                    exclusion_literals.append(temp_var)

            if exclusion_literals:
                self._model.add_bool_or([lit.Not() for lit in exclusion_literals])

            status = self._solver.solve(self._model)

        return GridBase.empty(), proposition_count

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        exclusion_literals = []
        for position, pipe in self._previous_solution:
            connected_to = pipe.get_connected_to()
            for direction, is_connected in [
                (Direction.up(), Direction.up() in connected_to),
                (Direction.down(), Direction.down() in connected_to),
                (Direction.left(), Direction.left() in connected_to),
                (Direction.right(), Direction.right() in connected_to),
            ]:
                temp_var = self._model.new_bool_var(f"prev_{position}_{direction}")
                self._model.add(self._grid_vars[position][direction] == is_connected).only_enforce_if(temp_var)
                self._model.add(self._grid_vars[position][direction] != is_connected).only_enforce_if(temp_var.Not())
                exclusion_literals.append(temp_var)

        if exclusion_literals:
            self._model.add_bool_or([lit.Not() for lit in exclusion_literals])

        return self.get_solution()

    def _add_constraints(self):
        self._add_possible_rotations_constraints()
        self._add_connected_constraints()
        self._add_tree_constraints()

    def _add_tree_constraints(self):
        # A tree with N nodes must have N-1 edges
        total_edges = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                # Each edge is shared between two cells.
                # To avoid double counting, only count right and down connections.
                pos_right = self._grid_vars.neighbor_right(pos)
                if pos_right is not None:
                    total_edges.append(self._grid_vars[pos][Direction.right()])
                pos_down = self._grid_vars.neighbor_down(pos)
                if pos_down is not None:
                    total_edges.append(self._grid_vars[pos][Direction.down()])

        self._model.add(sum(total_edges) == self._rows_number * self._columns_number - 1)

        # Potential constraints to avoid cycles and ensure connectivity (Spanning Tree)
        # We use a potential function: if (u,v) is an edge, then |pot[u] - pot[v]| = 1
        # This is a bit complex for a grid, let's use a flow-based approach instead.
        # Or a simpler distance-from-root approach.
        potentials = GridBase(
            [[self._model.new_int_var(0, self._rows_number * self._columns_number, f"pot_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        )

        # Pick one root (0,0) and set its potential to 0
        self._model.add(potentials[Position(0, 0)] == 0)

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                for direction in [Direction.up(), Direction.down(), Direction.left(), Direction.right()]:
                    neighbor_pos = pos.after(direction)
                    if neighbor_pos in self._grid_vars:
                        is_connected = self._grid_vars[pos][direction]
                        # If connected, potential of neighbor = potential of current + 1 OR vice versa
                        # Actually, to avoid cycles, we want a DAG structure from the root.
                        # so pot[neighbor] == pot[pos] + 1 IF pos is closer to root.
                        # But we don't know which one is closer.
                        # Let's say: if connected, pot[neighbor] != pot[pos]
                        self._model.add(potentials[pos] != potentials[neighbor_pos]).only_enforce_if(is_connected)
                        # To ensure it's a tree rooted at (0,0), every non-root node must have exactly
                        # one neighbor with potential = my_potential - 1.

                if pos != Position(0, 0):
                    # For each non-root node, there must be at least one incoming edge from a node with lower potential
                    incoming_edges = []
                    for direction in [Direction.up(), Direction.down(), Direction.left(), Direction.right()]:
                        neighbor_pos = pos.after(direction)
                        if neighbor_pos in self._grid_vars:
                            is_conn = self._grid_vars[pos][direction]
                            is_parent = self._model.new_bool_var(f"parent_{pos}_{direction}")
                            self._model.add(potentials[neighbor_pos] == potentials[pos] - 1).only_enforce_if(is_parent)
                            self._model.add(potentials[neighbor_pos] != potentials[pos] - 1).only_enforce_if(is_parent.Not())

                            parent_and_conn = self._model.new_bool_var(f"p_and_c_{pos}_{direction}")
                            self._model.add_bool_and([is_conn, is_parent]).only_enforce_if(parent_and_conn)
                            self._model.add_bool_or([is_conn.Not(), is_parent.Not()]).only_enforce_if(parent_and_conn.Not())
                            incoming_edges.append(parent_and_conn)

                    self._model.add_bool_or(incoming_edges)

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
            self._model.add(self._grid_vars[position][Direction.up()] == False)
        if position.r == self._input_grid.rows_number - 1:
            self._model.add(self._grid_vars[position][Direction.down()] == False)
        if position.c == 0:
            self._model.add(self._grid_vars[position][Direction.left()] == False)
        if position.c == self._input_grid.columns_number - 1:
            self._model.add(self._grid_vars[position][Direction.right()] == False)

    def _add_shape_l_constraint(self, pos: Position):
        # Create boolean variables for each L shape orientation
        l0 = self._model.new_bool_var(f"l0_{pos}")
        l1 = self._model.new_bool_var(f"l1_{pos}")
        l2 = self._model.new_bool_var(f"l2_{pos}")
        l3 = self._model.new_bool_var(f"l3_{pos}")

        # L shape: up and right connections
        self._model.add(self._grid_vars[pos][Direction.up()] == True).only_enforce_if(l0)
        self._model.add(self._grid_vars[pos][Direction.right()] == True).only_enforce_if(l0)
        self._model.add(self._grid_vars[pos][Direction.down()] == False).only_enforce_if(l0)
        self._model.add(self._grid_vars[pos][Direction.left()] == False).only_enforce_if(l0)

        # L shape: left and up connections
        self._model.add(self._grid_vars[pos][Direction.left()] == True).only_enforce_if(l1)
        self._model.add(self._grid_vars[pos][Direction.up()] == True).only_enforce_if(l1)
        self._model.add(self._grid_vars[pos][Direction.right()] == False).only_enforce_if(l1)
        self._model.add(self._grid_vars[pos][Direction.down()] == False).only_enforce_if(l1)

        # L shape: down and left connections
        self._model.add(self._grid_vars[pos][Direction.down()] == True).only_enforce_if(l2)
        self._model.add(self._grid_vars[pos][Direction.left()] == True).only_enforce_if(l2)
        self._model.add(self._grid_vars[pos][Direction.up()] == False).only_enforce_if(l2)
        self._model.add(self._grid_vars[pos][Direction.right()] == False).only_enforce_if(l2)

        # L shape: right and down connections
        self._model.add(self._grid_vars[pos][Direction.right()] == True).only_enforce_if(l3)
        self._model.add(self._grid_vars[pos][Direction.down()] == True).only_enforce_if(l3)
        self._model.add(self._grid_vars[pos][Direction.left()] == False).only_enforce_if(l3)
        self._model.add(self._grid_vars[pos][Direction.up()] == False).only_enforce_if(l3)

        # Exactly one of the L shapes must be true
        self._model.add_exactly_one([l0, l1, l2, l3])

    def add_shape_i_constraint(self, position):
        # Create boolean variables for each I shape orientation
        i0 = self._model.new_bool_var(f"i0_{position}")
        i1 = self._model.new_bool_var(f"i1_{position}")

        # I shape: vertical (up and down connections)
        self._model.add(self._grid_vars[position][Direction.up()] == True).only_enforce_if(i0)
        self._model.add(self._grid_vars[position][Direction.down()] == True).only_enforce_if(i0)
        self._model.add(self._grid_vars[position][Direction.left()] == False).only_enforce_if(i0)
        self._model.add(self._grid_vars[position][Direction.right()] == False).only_enforce_if(i0)

        # I shape: horizontal (left and right connections)
        self._model.add(self._grid_vars[position][Direction.left()] == True).only_enforce_if(i1)
        self._model.add(self._grid_vars[position][Direction.right()] == True).only_enforce_if(i1)
        self._model.add(self._grid_vars[position][Direction.up()] == False).only_enforce_if(i1)
        self._model.add(self._grid_vars[position][Direction.down()] == False).only_enforce_if(i1)

        # Exactly one of the I shapes must be true
        self._model.add_exactly_one([i0, i1])

    def add_shape_t_constraint(self, position):
        # Create boolean variables for each T shape orientation
        t0 = self._model.new_bool_var(f"t0_{position}")
        t1 = self._model.new_bool_var(f"t1_{position}")
        t2 = self._model.new_bool_var(f"t2_{position}")
        t3 = self._model.new_bool_var(f"t3_{position}")

        # T shape: down, left, right connections (upside-down T)
        self._model.add(self._grid_vars[position][Direction.down()] == True).only_enforce_if(t0)
        self._model.add(self._grid_vars[position][Direction.left()] == True).only_enforce_if(t0)
        self._model.add(self._grid_vars[position][Direction.right()] == True).only_enforce_if(t0)
        self._model.add(self._grid_vars[position][Direction.up()] == False).only_enforce_if(t0)

        # T shape: right, up, down connections (T facing right)
        self._model.add(self._grid_vars[position][Direction.right()] == True).only_enforce_if(t1)
        self._model.add(self._grid_vars[position][Direction.up()] == True).only_enforce_if(t1)
        self._model.add(self._grid_vars[position][Direction.down()] == True).only_enforce_if(t1)
        self._model.add(self._grid_vars[position][Direction.left()] == False).only_enforce_if(t1)

        # T shape: up, right, left connections (T facing up)
        self._model.add(self._grid_vars[position][Direction.up()] == True).only_enforce_if(t2)
        self._model.add(self._grid_vars[position][Direction.right()] == True).only_enforce_if(t2)
        self._model.add(self._grid_vars[position][Direction.left()] == True).only_enforce_if(t2)
        self._model.add(self._grid_vars[position][Direction.down()] == False).only_enforce_if(t2)

        # T shape: left, down, up connections (T facing left)
        self._model.add(self._grid_vars[position][Direction.left()] == True).only_enforce_if(t3)
        self._model.add(self._grid_vars[position][Direction.down()] == True).only_enforce_if(t3)
        self._model.add(self._grid_vars[position][Direction.up()] == True).only_enforce_if(t3)
        self._model.add(self._grid_vars[position][Direction.right()] == False).only_enforce_if(t3)

        # Exactly one of the T shapes must be true
        self._model.add_exactly_one([t0, t1, t2, t3])

    def add_shape_e_constraint(self, position):
        # Create boolean variables for each E shape orientation (endpoint)
        e0 = self._model.new_bool_var(f"e0_{position}")
        e1 = self._model.new_bool_var(f"e1_{position}")
        e2 = self._model.new_bool_var(f"e2_{position}")
        e3 = self._model.new_bool_var(f"e3_{position}")

        # E shape: only up connection
        self._model.add(self._grid_vars[position][Direction.up()] == True).only_enforce_if(e0)
        self._model.add(self._grid_vars[position][Direction.down()] == False).only_enforce_if(e0)
        self._model.add(self._grid_vars[position][Direction.left()] == False).only_enforce_if(e0)
        self._model.add(self._grid_vars[position][Direction.right()] == False).only_enforce_if(e0)

        # E shape: only left connection
        self._model.add(self._grid_vars[position][Direction.left()] == True).only_enforce_if(e1)
        self._model.add(self._grid_vars[position][Direction.right()] == False).only_enforce_if(e1)
        self._model.add(self._grid_vars[position][Direction.up()] == False).only_enforce_if(e1)
        self._model.add(self._grid_vars[position][Direction.down()] == False).only_enforce_if(e1)

        # E shape: only down connection
        self._model.add(self._grid_vars[position][Direction.down()] == True).only_enforce_if(e2)
        self._model.add(self._grid_vars[position][Direction.up()] == False).only_enforce_if(e2)
        self._model.add(self._grid_vars[position][Direction.left()] == False).only_enforce_if(e2)
        self._model.add(self._grid_vars[position][Direction.right()] == False).only_enforce_if(e2)

        # E shape: only right connection
        self._model.add(self._grid_vars[position][Direction.right()] == True).only_enforce_if(e3)
        self._model.add(self._grid_vars[position][Direction.left()] == False).only_enforce_if(e3)
        self._model.add(self._grid_vars[position][Direction.up()] == False).only_enforce_if(e3)
        self._model.add(self._grid_vars[position][Direction.down()] == False).only_enforce_if(e3)

        # Exactly one of the E shapes must be true
        self._model.add_exactly_one([e0, e1, e2, e3])

    def _add_connected_constraints(self):
        for position, value in self._grid_vars:
            position_up = self._grid_vars.neighbor_up(position)
            position_down = self._grid_vars.neighbor_down(position)
            position_left = self._grid_vars.neighbor_left(position)
            position_right = self._grid_vars.neighbor_right(position)
            if position_up is not None:
                self._model.add(self._grid_vars[position][Direction.up()] == self._grid_vars[position_up][Direction.down()])
            if position_down is not None:
                self._model.add(self._grid_vars[position][Direction.down()] == self._grid_vars[position_down][Direction.up()])
            if position_left is not None:
                self._model.add(self._grid_vars[position][Direction.left()] == self._grid_vars[position_left][Direction.right()])
            if position_right is not None:
                self._model.add(self._grid_vars[position][Direction.right()] == self._grid_vars[position_right][Direction.left()])

    def _create_pipe_from_model(self, position: Position):
        directions = []
        if self._solver.value(self._grid_vars[position][Direction.up()]):
            directions.append(Direction.up())
        if self._solver.value(self._grid_vars[position][Direction.left()]):
            directions.append(Direction.left())
        if self._solver.value(self._grid_vars[position][Direction.down()]):
            directions.append(Direction.down())
        if self._solver.value(self._grid_vars[position][Direction.right()]):
            directions.append(Direction.right())
        return Pipe.from_connection(frozenset(directions))
