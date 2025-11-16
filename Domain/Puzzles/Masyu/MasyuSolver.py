from ortools.sat.cp_model_pb2 import CpSolverStatus
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar, CpModel, CpSolver

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class MasyuSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._model = CpModel()
        self._solver = CpSolver()
        self._initialized = False
        self._island_bridges_z3: dict[Position, dict[Direction, IntVar]] = {}
        self._previous_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])

    def _init_solver(self):
        self._model = cp_model.CpModel()
        self._island_bridges_z3 = {
            island.position: {direction: self._model.NewBoolVar(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()} for island in self._island_grid.islands.values()
        }
        self._add_constraints()
        self._initialized = True

    @staticmethod
    def _is_feasible(status: CpSolverStatus) -> bool:
        return status in (cp_model.OPTIMAL, cp_model.FEASIBLE)

    def get_solution(self) -> IslandGrid:
        if not self._initialized:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._is_feasible(self._solver.Solve(self._model)):
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, var in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = self._solver.Value(var)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            # Block this exact set of active edges for each detected loop
            for positions in connected_positions:
                literals = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        if value == 1:
                            literals.append(self._island_bridges_z3[position][direction])
                if literals:
                    self._model.AddBoolOr([lit.Not() for lit in literals])
            self.init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        literals = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                if value == 1:
                    literals.append(self._island_bridges_z3[island.position][direction])
        if literals:
            self._model.AddBoolOr([lit.Not() for lit in literals])

        self.init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_dots_constraints()

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    neighbor_pos = island.direction_position_bridges[direction][0]
                    self._model.Add(self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[neighbor_pos][direction.opposite])
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            vars_list = [self._island_bridges_z3[island.position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]
            s = sum(vars_list)
            is0 = self._model.NewBoolVar(f"sum0_{island.position}")
            is2 = self._model.NewBoolVar(f"sum2_{island.position}")
            # s == 0 or s == 2
            self._model.Add(s == 0).OnlyEnforceIf(is0)
            self._model.Add(s != 0).OnlyEnforceIf(is0.Not())
            self._model.Add(s == 2).OnlyEnforceIf(is2)
            self._model.Add(s != 2).OnlyEnforceIf(is2.Not())
            self._model.AddBoolOr([is0, is2])

    def _add_dots_constraints(self):
        for position, value in self.input_grid:
            if value == 'w':
                # White: path goes straight through and turns in the next cell
                h_possible = None
                v_possible = None
                # Horizontal case
                if position.left in self._island_bridges_z3 and position.right in self._island_bridges_z3:
                    h_possible = self._model.NewBoolVar(f"w_h_{position}")
                    self._model.Add(self._island_bridges_z3[position][Direction.left()] == 1).OnlyEnforceIf(h_possible)
                    self._model.Add(self._island_bridges_z3[position][Direction.right()] == 1).OnlyEnforceIf(h_possible)
                    turn_literals = []
                    if Direction.up() in self._island_bridges_z3[position.left]:
                        turn_literals.append(self._island_bridges_z3[position.left][Direction.up()])
                    if Direction.down() in self._island_bridges_z3[position.left]:
                        turn_literals.append(self._island_bridges_z3[position.left][Direction.down()])
                    if Direction.up() in self._island_bridges_z3[position.right]:
                        turn_literals.append(self._island_bridges_z3[position.right][Direction.up()])
                    if Direction.down() in self._island_bridges_z3[position.right]:
                        turn_literals.append(self._island_bridges_z3[position.right][Direction.down()])
                    if turn_literals:
                        self._model.AddBoolOr(turn_literals).OnlyEnforceIf(h_possible)
                    else:
                        # If no possible turn, disable this option
                        self._model.Add(h_possible == 0)
                # Vertical case
                if position.up in self._island_bridges_z3 and position.down in self._island_bridges_z3:
                    v_possible = self._model.NewBoolVar(f"w_v_{position}")
                    self._model.Add(self._island_bridges_z3[position][Direction.up()] == 1).OnlyEnforceIf(v_possible)
                    self._model.Add(self._island_bridges_z3[position][Direction.down()] == 1).OnlyEnforceIf(v_possible)
                    turn_literals = []
                    if Direction.left() in self._island_bridges_z3[position.up]:
                        turn_literals.append(self._island_bridges_z3[position.up][Direction.left()])
                    if Direction.right() in self._island_bridges_z3[position.up]:
                        turn_literals.append(self._island_bridges_z3[position.up][Direction.right()])
                    if Direction.left() in self._island_bridges_z3[position.down]:
                        turn_literals.append(self._island_bridges_z3[position.down][Direction.left()])
                    if Direction.right() in self._island_bridges_z3[position.down]:
                        turn_literals.append(self._island_bridges_z3[position.down][Direction.right()])
                    if turn_literals:
                        self._model.AddBoolOr(turn_literals).OnlyEnforceIf(v_possible)
                    else:
                        self._model.Add(v_possible == 0)
                # At least one orientation must be taken
                choices = []
                if h_possible is not None:
                    choices.append(h_possible)
                if v_possible is not None:
                    choices.append(v_possible)
                if choices:
                    self._model.AddBoolOr(choices)
            if value == 'b':
                # Black: must turn on the dot, and go straight both before and after at least one cell
                patterns = []
                # right + down
                if position.right in self._island_bridges_z3 and position.right.right in self._island_bridges_z3 and position.down in self._island_bridges_z3 and position.down.down in self._island_bridges_z3:
                    p = self._model.NewBoolVar(f"b_rd_{position}")
                    self._model.Add(self._island_bridges_z3[position][Direction.right()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position.right][Direction.right()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position][Direction.down()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position.down][Direction.down()] == 1).OnlyEnforceIf(p)
                    patterns.append(p)
                # left + down
                if position.left in self._island_bridges_z3 and position.left.left in self._island_bridges_z3 and position.down in self._island_bridges_z3 and position.down.down in self._island_bridges_z3:
                    p = self._model.NewBoolVar(f"b_ld_{position}")
                    self._model.Add(self._island_bridges_z3[position][Direction.left()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position.left][Direction.left()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position][Direction.down()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position.down][Direction.down()] == 1).OnlyEnforceIf(p)
                    patterns.append(p)
                # right + up
                if position.right in self._island_bridges_z3 and position.right.right in self._island_bridges_z3 and position.up in self._island_bridges_z3 and position.up.up in self._island_bridges_z3:
                    p = self._model.NewBoolVar(f"b_ru_{position}")
                    self._model.Add(self._island_bridges_z3[position][Direction.right()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position.right][Direction.right()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position][Direction.up()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position.up][Direction.up()] == 1).OnlyEnforceIf(p)
                    patterns.append(p)
                # left + up
                if position.left in self._island_bridges_z3 and position.left.left in self._island_bridges_z3 and position.up in self._island_bridges_z3 and position.up.up in self._island_bridges_z3:
                    p = self._model.NewBoolVar(f"b_lu_{position}")
                    self._model.Add(self._island_bridges_z3[position][Direction.left()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position.left][Direction.left()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position][Direction.up()] == 1).OnlyEnforceIf(p)
                    self._model.Add(self._island_bridges_z3[position.up][Direction.up()] == 1).OnlyEnforceIf(p)
                    patterns.append(p)
                if patterns:
                    self._model.AddBoolOr(patterns)
