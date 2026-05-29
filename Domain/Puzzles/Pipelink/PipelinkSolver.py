from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class PipelinkSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._rows_number, self._columns_number = grid.rows_number, grid.columns_number
        self._island_grid: IslandGrid | None = None
        self._model = cp_model.CpModel()
        self._cp_solver = cp_model.CpSolver()
        self._grid_z3: Grid | None = None
        self._previous_solution: IslandGrid
        self._solver_initialized = False

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self._columns_number)] for r in range(self._rows_number)])

    def _init_solver(self):
        self._grid_z3 = Grid(
            [[{direction: self._model.NewBoolVar(f"{direction}_{r}-{c}") for direction in Direction.orthogonal_directions()} for c in range(self._columns_number)] for r in
             range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        propositions_count = 0
        while self._cp_solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            self._init_island_grid()
            propositions_count += 1
            for position, direction_bridges in self._grid_z3:
                for direction, bridges in direction_bridges.items():
                    bridges_number = 1 if self._cp_solver.Value(bridges) else 0
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            connected_positions = self._island_grid.compute_linear_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, propositions_count

            biggest_connected_positions = max(connected_positions, key=len)
            connected_positions.remove(biggest_connected_positions)
            for positions in connected_positions:
                block_literals = []
                for position in positions:
                    for direction in self._island_grid[position].direction_position_bridges.keys():
                        block_literals.append(self._grid_z3[position][direction].Not())
                    for direction in Direction.orthogonal_directions():
                        if direction not in self._island_grid[position].direction_position_bridges:
                            block_literals.append(self._grid_z3[position][direction])
                self._model.AddBoolOr(block_literals)

        return IslandGrid.empty(), propositions_count

    def get_other_solution(self):
        eq_bools = []
        for i, (position, island) in enumerate(self._previous_solution):
            for direction in Direction.orthogonal_directions():
                bridge_value = island.direction_position_bridges.get(direction, [0, 0])[1]
                expected = bridge_value == 1
                b = self._model.NewBoolVar(f'prev_eq_{i}_{direction}')
                var = self._grid_z3[position][direction]
                self._model.Add(var == int(expected)).OnlyEnforceIf(b)
                self._model.Add(var != int(expected)).OnlyEnforceIf(b.Not())
                eq_bools.append(b)
        self._model.Add(sum(eq_bools) <= len(eq_bools) - 1)
        self._solver_initialized = True
        return self.get_solution()

    def get_stats(self) -> dict:
        return {
            "num_conflicts": self._cp_solver.NumConflicts(),
            "num_branches": self._cp_solver.NumBranches(),
            "wall_time": self._cp_solver.WallTime(),
        }

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_opposite_constraints()
        self._add_bridges_sum_constraints()

    def _add_initials_constraints(self):
        for position in self._grid_z3.edge_up_positions():
            self._model.Add(self._grid_z3[position][Direction.up()] == 0)
        for position in self._grid_z3.edge_down_positions():
            self._model.Add(self._grid_z3[position][Direction.down()] == 0)
        for position in self._grid_z3.edge_left_positions():
            self._model.Add(self._grid_z3[position][Direction.left()] == 0)
        for position in self._grid_z3.edge_right_positions():
            self._model.Add(self._grid_z3[position][Direction.right()] == 0)

        for position, island in [(position, island) for position, island in self.input_grid if not island.has_no_bridge()]:
            for direction, (_, bridges) in island.direction_position_bridges.items():
                self._model.Add(self._grid_z3[position][direction] == (bridges == 1))

    def _add_opposite_constraints(self):
        for position, _ in self._grid_z3:
            if position.up in self._grid_z3:
                self._model.Add(self._grid_z3[position][Direction.up()] == self._grid_z3[position.up][Direction.down()])
            if position.down in self._grid_z3:
                self._model.Add(self._grid_z3[position][Direction.down()] == self._grid_z3[position.down][Direction.up()])
            if position.left in self._grid_z3:
                self._model.Add(self._grid_z3[position][Direction.left()] == self._grid_z3[position.left][Direction.right()])
            if position.right in self._grid_z3:
                self._model.Add(self._grid_z3[position][Direction.right()] == self._grid_z3[position.right][Direction.left()])

    def _add_bridges_sum_constraints(self):
        for position, _ in self._grid_z3:
            vars_list = [self._grid_z3[position][direction] for direction in Direction.orthogonal_directions()]
            b2 = self._model.NewBoolVar(f'sum2_{position.r}_{position.c}')
            b4 = self._model.NewBoolVar(f'sum4_{position.r}_{position.c}')
            self._model.Add(sum(vars_list) == 2).OnlyEnforceIf(b2)
            self._model.Add(sum(vars_list) != 2).OnlyEnforceIf(b2.Not())
            self._model.Add(sum(vars_list) == 4).OnlyEnforceIf(b4)
            self._model.Add(sum(vars_list) != 4).OnlyEnforceIf(b4.Not())
            self._model.AddBoolOr([b2, b4])
