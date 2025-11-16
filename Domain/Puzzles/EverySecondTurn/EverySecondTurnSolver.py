from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

X = '*'
_ = '.'


class EverySecondTurnSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._model = cp_model.CpModel()
        self._island_bridges: dict[Position, dict[Direction, cp_model.BoolVar]] = {}
        self._previous_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._input_grid.columns_number)] for r in
             range(self._input_grid.rows_number)]
        )

    def _init_solver(self):
        self._island_bridges = {
            island.position: {direction: self._model.NewBoolVar(f"{island.position}_{direction}") for direction in
                              Direction.orthogonal_directions()}
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._model.Proto().variables:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        solver = cp_model.CpSolver()
        while solver.Solve(self._model) == cp_model.OPTIMAL:
            proposition_count += 1
            for position, direction_bridges in self._island_bridges.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges:
                        continue
                    bridges_number = solver.Value(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(
                            self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[
                        position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            not_loop_constraints = []
            for positions in connected_positions:
                cell_constraints = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        cell_constraints.append(self._island_bridges[position][direction])
                not_loop_constraints.append(cell_constraints)
            for constraint in not_loop_constraints:
                self._model.AddBoolOr([c.Not() for c in constraint])
            self.init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges[island.position][direction])
        self._model.AddBoolOr([c.Not() for c in previous_solution_constraints])

        self.init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_links_constraints()
        self._add_turn_at_every_circle_constraints()

    def _add_initial_constraints(self):
        for position, direction_bridges in self._island_bridges.items():
            bridges_count_vars = list(direction_bridges.values())
            self._model.Add(sum(bridges_count_vars) == 2)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(
                        self._island_bridges[island.position][direction] ==
                        self._island_bridges[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._model.Add(self._island_bridges[island.position][direction] == 0)

    def _add_links_constraints(self):
        for position in [position for position, value in self._input_grid if value == X]:
            linked_circles_constraints = self._one_turn_between_linked_circles_constraints(position)
            self._model.Add(sum(linked_circles_constraints) == 2)

    def _one_turn_between_linked_circles_constraints(self, circle_pos: Position) -> list:
        constraints = []
        for other_circle_pos in [pos for pos, value in self._input_grid if
                                 value == X and pos.r != circle_pos.r and pos.c != circle_pos.c]:
            hor_turn_pos = Position(circle_pos.r, other_circle_pos.c)
            vert_turn_pos = Position(other_circle_pos.r, circle_pos.c)
            hor_direction = Direction.right() if other_circle_pos.c > circle_pos.c else Direction.left()
            vert_direction = Direction.down() if other_circle_pos.r > circle_pos.r else Direction.up()

            hor_path_vars = self._to_other_circle_constraint(circle_pos, other_circle_pos, hor_turn_pos,
                                                                    hor_direction, vert_direction)
            vert_path_vars = self._to_other_circle_constraint(circle_pos, other_circle_pos, vert_turn_pos,
                                                                      vert_direction, hor_direction)

            hor_path_ok = self.new_and(hor_path_vars)
            vert_path_ok = self.new_and(vert_path_vars)

            link_ok = self._model.NewBoolVar(f"link_{circle_pos}_to_{other_circle_pos}")
            self._model.AddBoolOr([hor_path_ok, vert_path_ok]).OnlyEnforceIf(link_ok)
            self._model.AddImplication(hor_path_ok, link_ok)
            self._model.AddImplication(vert_path_ok, link_ok)

            constraints.append(link_ok)

        return constraints

    def _to_other_circle_constraint(self, circle_pos, other_circle_pos, turn_position, first_direction,
                                    second_direction) -> list:
        constraints = [self._island_bridges[circle_pos][first_direction]]
        current_position = circle_pos.after(first_direction)
        while self._input_grid[current_position] == _ and current_position != turn_position:
            constraints.append(self._island_bridges[current_position][first_direction])
            current_position = current_position.after(first_direction)
        if self._input_grid[current_position] != _:
            b = self._model.NewBoolVar("")
            self._model.Add(b == 0)
            return [b]

        constraints.append(self._island_bridges[current_position][second_direction])
        current_position = current_position.after(second_direction)
        while self._input_grid[current_position] == _ and current_position != other_circle_pos:
            constraints.append(self._island_bridges[current_position][second_direction])
            current_position = current_position.after(second_direction)
        if current_position != other_circle_pos:
            b = self._model.NewBoolVar("")
            self._model.Add(b == 0)
            return [b]

        return constraints

    def _add_turn_at_every_circle_constraints(self):
        for position in [position for position, value in self._input_grid if value == X]:
            right = self._island_bridges[position][Direction.right()]
            up = self._island_bridges[position][Direction.up()]
            left = self._island_bridges[position][Direction.left()]
            down = self._island_bridges[position][Direction.down()]

            self._model.AddBoolOr([
                self.new_and([right, up, left.Not(), down.Not()]),
                self.new_and([right, up.Not(), left.Not(), down]),
                self.new_and([right.Not(), up.Not(), left, down]),
                self.new_and([right.Not(), up, left, down.Not()])
            ])

    def new_and(self, literals):
        b = self._model.NewBoolVar('')
        if not literals:
            self._model.Add(b == 1)
            return b
        for lit in literals:
            self._model.AddImplication(b, lit)
        self._model.AddBoolOr([l.Not() for l in literals] + [b])
        return b
