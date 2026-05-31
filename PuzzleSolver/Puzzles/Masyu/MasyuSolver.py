from ortools.sat.cp_model_pb2 import CpSolverStatus
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar, CpModel, CpSolver

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class MasyuSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._model = CpModel()
        self._solver = CpSolver()
        self._initialized = False
        self._island_bridges_var: dict[Position, dict[Direction, IntVar]] = {}
        self._previous_solution: IslandGrid | None = None
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])
        self._model = cp_model.CpModel()
        self._island_bridges_var = {
            island.position: {direction: self._model.new_bool_var(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()} for island in self._island_grid.islands.values()
        }
        self._add_constraints()
        self._initialized = True

    def get_solution(self) -> IslandGrid:
        if self._solver.solve(self._model) not in (CpSolverStatus.OPTIMAL, CpSolverStatus.FEASIBLE) :
            return IslandGrid.empty()
        self._extract_solution()
        return self._island_grid

    def _extract_solution(self):
        for position, direction_bridges in self._island_bridges_var.items():
            for direction, var in direction_bridges.items():
                if position.after(direction) not in self._island_bridges_var:
                    continue
                bridges_number = self._solver.value(var)
                if bridges_number > 0:
                    self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                    self._island_grid[position].direction_position_bridges.pop(direction)
            self._island_grid[position].set_bridges_count_according_to_directions_bridges()
        self._previous_solution = self._island_grid

    def get_other_solution(self):
        literals = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                if value == 1:
                    literals.append(self._island_bridges_var[island.position][direction])
        self._model.add_bool_or([lit.negated() for lit in literals])

        return self.get_solution()

    def _add_constraints(self):
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_no_small_square_loops_constraints()
        self._add_dots_constraints()
        self._add_circuit_constraint()

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    neighbor_pos = island.direction_position_bridges[direction][0]
                    self._model.add(self._island_bridges_var[island.position][direction] == self._island_bridges_var[neighbor_pos][direction.opposite])
                else:
                    self._model.add(self._island_bridges_var[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            vars_list = [self._island_bridges_var[island.position][direction] for direction in Direction.orthogonal_directions()]
            s = self._model.new_int_var(0, 4, f"sum_{island.position}")
            self._model.add(s == sum(vars_list))
            self._model.add_allowed_assignments([s], [(0,), (2,)])

    def _add_no_small_loops_constraints(self):
        rows = self.input_grid.rows_number
        cols = self.input_grid.columns_number
        for height in range(2, 5):
            for width in range(2, 5):
                if height == 2 and width == 2:
                    continue
                for r in range(rows - height + 1):
                    for c in range(cols - width + 1):
                        edges = []
                        for j in range(width - 1):
                            edges.append(self._island_bridges_var[Position(r, c + j)][Direction.right()])
                            edges.append(self._island_bridges_var[Position(r + height - 1, c + j)][Direction.right()])
                        for i in range(height - 1):
                            edges.append(self._island_bridges_var[Position(r + i, c)][Direction.down()])
                            edges.append(self._island_bridges_var[Position(r + i, c + width - 1)][Direction.down()])
                        self._model.add(sum(edges) <= 2 * (height + width - 2) - 1)

    def _add_no_small_square_loops_constraints(self):
        for r in range(self.input_grid.rows_number - 1):
            for c in range(self.input_grid.columns_number - 1):
                edges = [
                    self._island_bridges_var[Position(r, c)][Direction.right()],
                    self._island_bridges_var[Position(r, c + 1)][Direction.down()],
                    self._island_bridges_var[Position(r + 1, c + 1)][Direction.left()],
                    self._island_bridges_var[Position(r + 1, c)][Direction.up()],
                ]
                self._model.add(sum(edges) <= 3)

    def _add_dots_constraints(self):
        for position, value in self.input_grid:
            if value == 'w':
                # White: path goes straight through and turns in the next cell
                h_possible = None
                v_possible = None
                # Horizontal case
                if position.left in self._island_bridges_var and position.right in self._island_bridges_var:
                    h_possible = self._model.new_bool_var(f"w_h_{position}")
                    self._model.add(self._island_bridges_var[position][Direction.left()] == 1).only_enforce_if(h_possible)
                    self._model.add(self._island_bridges_var[position][Direction.right()] == 1).only_enforce_if(h_possible)
                    turn_literals = []
                    if Direction.up() in self._island_bridges_var[position.left]:
                        turn_literals.append(self._island_bridges_var[position.left][Direction.up()])
                    if Direction.down() in self._island_bridges_var[position.left]:
                        turn_literals.append(self._island_bridges_var[position.left][Direction.down()])
                    if Direction.up() in self._island_bridges_var[position.right]:
                        turn_literals.append(self._island_bridges_var[position.right][Direction.up()])
                    if Direction.down() in self._island_bridges_var[position.right]:
                        turn_literals.append(self._island_bridges_var[position.right][Direction.down()])
                    if turn_literals:
                        self._model.add_bool_or(turn_literals).only_enforce_if(h_possible)
                    else:
                        # If no possible turn, disable this option
                        self._model.add(h_possible == 0)
                # Vertical case
                if position.up in self._island_bridges_var and position.down in self._island_bridges_var:
                    v_possible = self._model.new_bool_var(f"w_v_{position}")
                    self._model.add(self._island_bridges_var[position][Direction.up()] == 1).only_enforce_if(v_possible)
                    self._model.add(self._island_bridges_var[position][Direction.down()] == 1).only_enforce_if(v_possible)
                    turn_literals = []
                    if Direction.left() in self._island_bridges_var[position.up]:
                        turn_literals.append(self._island_bridges_var[position.up][Direction.left()])
                    if Direction.right() in self._island_bridges_var[position.up]:
                        turn_literals.append(self._island_bridges_var[position.up][Direction.right()])
                    if Direction.left() in self._island_bridges_var[position.down]:
                        turn_literals.append(self._island_bridges_var[position.down][Direction.left()])
                    if Direction.right() in self._island_bridges_var[position.down]:
                        turn_literals.append(self._island_bridges_var[position.down][Direction.right()])
                    if turn_literals:
                        self._model.add_bool_or(turn_literals).only_enforce_if(v_possible)
                    else:
                        self._model.add(v_possible == 0)
                # At least one orientation must be taken
                choices = []
                if h_possible is not None:
                    choices.append(h_possible)
                if v_possible is not None:
                    choices.append(v_possible)
                if choices:
                    self._model.add_bool_or(choices)
            if value == 'b':
                # Black: must turn on the dot, and go straight both before and after at least one cell
                patterns = []
                # right + down
                if position.right in self._island_bridges_var and position.right.right in self._island_bridges_var and position.down in self._island_bridges_var and position.down.down in self._island_bridges_var:
                    p = self._model.new_bool_var(f"b_rd_{position}")
                    self._model.add(self._island_bridges_var[position][Direction.right()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position.right][Direction.right()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position][Direction.down()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position.down][Direction.down()] == 1).only_enforce_if(p)
                    patterns.append(p)
                # left + down
                if position.left in self._island_bridges_var and position.left.left in self._island_bridges_var and position.down in self._island_bridges_var and position.down.down in self._island_bridges_var:
                    p = self._model.new_bool_var(f"b_ld_{position}")
                    self._model.add(self._island_bridges_var[position][Direction.left()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position.left][Direction.left()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position][Direction.down()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position.down][Direction.down()] == 1).only_enforce_if(p)
                    patterns.append(p)
                # right + up
                if position.right in self._island_bridges_var and position.right.right in self._island_bridges_var and position.up in self._island_bridges_var and position.up.up in self._island_bridges_var:
                    p = self._model.new_bool_var(f"b_ru_{position}")
                    self._model.add(self._island_bridges_var[position][Direction.right()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position.right][Direction.right()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position][Direction.up()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position.up][Direction.up()] == 1).only_enforce_if(p)
                    patterns.append(p)
                # left + up
                if position.left in self._island_bridges_var and position.left.left in self._island_bridges_var and position.up in self._island_bridges_var and position.up.up in self._island_bridges_var:
                    p = self._model.new_bool_var(f"b_lu_{position}")
                    self._model.add(self._island_bridges_var[position][Direction.left()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position.left][Direction.left()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position][Direction.up()] == 1).only_enforce_if(p)
                    self._model.add(self._island_bridges_var[position.up][Direction.up()] == 1).only_enforce_if(p)
                    patterns.append(p)
                if patterns:
                    self._model.add_bool_or(patterns)

    def _add_circuit_constraint(self):
        cols = self.input_grid.columns_number
        arcs = []
        for pos, island in self._island_grid.islands.items():
            u = pos.r * cols + pos.c
            for direction, (neighbor_pos, _) in island.direction_position_bridges.items():
                if direction not in (Direction.right(), Direction.down()):
                    continue
                v = neighbor_pos.r * cols + neighbor_pos.c
                bridge_var = self._island_bridges_var[pos][direction]
                arc_uv = self._model.new_bool_var(f"arc_{u}_{v}")
                arc_vu = self._model.new_bool_var(f"arc_{v}_{u}")
                self._model.add(arc_uv + arc_vu == bridge_var)
                arcs.append((u, v, arc_uv))
                arcs.append((v, u, arc_vu))
        for pos in self._island_grid.islands:
            u = pos.r * cols + pos.c
            bv_sum = sum(self._island_bridges_var[pos][d] for d in Direction.orthogonal_directions())
            is_inactive = self._model.new_bool_var(f"inactive_{u}")
            self._model.add(bv_sum == 0).only_enforce_if(is_inactive)
            self._model.add(bv_sum == 2).only_enforce_if(is_inactive.Not())
            self_loop = self._model.new_bool_var(f"self_loop_{u}")
            self._model.add(self_loop == 1).only_enforce_if(is_inactive)
            self._model.add(self_loop == 0).only_enforce_if(is_inactive.Not())
            arcs.append((u, u, self_loop))
        if arcs:
            self._model.add_circuit(arcs)
