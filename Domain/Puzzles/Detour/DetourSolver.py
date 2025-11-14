from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class DetourSolver(GameSolver):
    empty = None

    def __init__(self, clues_grid: Grid, regions_grid: Grid):
        self._clues_grid = clues_grid
        self._regions_grid = regions_grid
        self._regions = regions_grid.get_regions()
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._island_bridges: dict[Position, dict[Direction, cp_model.BoolVar]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._clues_grid.columns_number)] for r in range(self._clues_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges = {island.position: {direction: self._model.NewBoolVar(f"{island.position}_{direction}") for direction in Direction.orthogonals()} for island in
                                   self._island_grid.islands.values()}
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
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=False)
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
            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges[island.position][direction])
        self._model.AddBoolOr([c.Not() for c in previous_solution_constraints])

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_clues_turn_regions_constraints()

    def _add_initial_constraints(self):
        for r in range(self._island_grid.rows_number):
            self._model.Add(self._island_bridges[Position(r, 0)][Direction.left()] == 0)
            self._model.Add(self._island_bridges[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0)
        for c in range(self._island_grid.columns_number):
            self._model.Add(self._island_bridges[Position(0, c)][Direction.up()] == 0)
            self._model.Add(self._island_bridges[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(
                        self._island_bridges[island.position][direction] == self._island_bridges[island.direction_position_bridges[direction][0]][
                            direction.opposite])
                else:
                    self._model.Add(self._island_bridges[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            sum2_constraint = sum([self._island_bridges[island.position][direction] for direction in Direction.orthogonals()]) == 2
            self._model.Add(sum2_constraint)

    def _add_clues_turn_regions_constraints(self):
        for region in self._regions.values():
            self._add_clues_turn_region_constraints(region)

    def _add_clues_turn_region_constraints(self, region: frozenset[Position]):
        turn_clue = max(clue if (clue:=self._clues_grid[position]) != self.empty else 0 for position in region)

        turn_regions = []
        for position in region:
            right = self._island_bridges[position][Direction.right()]
            up = self._island_bridges[position][Direction.up()]
            left = self._island_bridges[position][Direction.left()]
            down = self._island_bridges[position][Direction.down()]

            b = self._model.NewBoolVar('')
            self._model.AddBoolOr([
                self.new_and([right, up, left.Not(), down.Not()]),
                self.new_and([right, up.Not(), left.Not(), down]),
                self.new_and([right.Not(), up.Not(), left, down]),
                self.new_and([right.Not(), up, left, down.Not()])
            ]).OnlyEnforceIf(b)
            self._model.AddImplication(b.Not(), self.new_and([right, up, left.Not(), down.Not()]).Not())
            self._model.AddImplication(b.Not(), self.new_and([right, up.Not(), left.Not(), down]).Not())
            self._model.AddImplication(b.Not(), self.new_and([right.Not(), up.Not(), left, down]).Not())
            self._model.AddImplication(b.Not(), self.new_and([right.Not(), up, left, down.Not()]).Not())

            turn_regions.append(b)
        self._model.Add(sum(turn_regions) == turn_clue)

    def new_and(self, literals):
        b = self._model.NewBoolVar('')
        if not literals:
            self._model.Add(b == 1)
            return b
        for lit in literals:
            self._model.AddImplication(b, lit)
        self._model.AddBoolOr([l.Not() for l in literals] + [b])
        return b
