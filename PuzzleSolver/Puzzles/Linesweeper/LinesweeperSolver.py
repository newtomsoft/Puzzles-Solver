from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class LinesweeperSolver(GameSolver):
    def __init__(self, grid: Grid):
        super().__init__()
        self._input_grid = grid
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._model = cp_model.CpModel()
        self._island_bridges_z3: dict[Position, dict[Direction, cp_model.IntVar]] = {}
        self._previous_solution: IslandGrid | None = None
        self._solver_initialized = False

    def init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._input_grid.columns_number)] for r in
             range(self._input_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {direction: self._model.NewIntVar(0, 1, f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()}
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = self._solver.Value(bridges)
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

            for positions in connected_positions:
                eq_bools = []
                for i, position in enumerate(positions):
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        b = self._model.NewBoolVar(f'eq_conn_{i}_{position}_{direction}')
                        var = self._island_bridges_z3[position][direction]
                        self._model.Add(var == value).OnlyEnforceIf(b)
                        self._model.Add(var != value).OnlyEnforceIf(b.Not())
                        eq_bools.append(b)
                self._model.Add(sum(eq_bools) <= len(eq_bools) - 1)
            self.init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        eq_bools = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                var = self._island_bridges_z3[island.position][direction]
                b = self._model.NewBoolVar(f'prev_eq_{island.position}_{direction}')
                self._model.Add(var == value).OnlyEnforceIf(b)
                self._model.Add(var != value).OnlyEnforceIf(b.Not())
                eq_bools.append(b)
        self._model.Add(sum(eq_bools) <= len(eq_bools) - 1)

        self.init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()

    def _add_initial_constraints(self):
        for position, direction_bridges in self._island_bridges_z3.items():
            bridges_count_vars = list(direction_bridges.values())
            b0 = self._model.NewBoolVar(f'sum0_{position}')
            b2 = self._model.NewBoolVar(f'sum2_{position}')
            self._model.Add(sum(bridges_count_vars) == 0).OnlyEnforceIf(b0)
            self._model.Add(sum(bridges_count_vars) != 0).OnlyEnforceIf(b0.Not())
            self._model.Add(sum(bridges_count_vars) == 2).OnlyEnforceIf(b2)
            self._model.Add(sum(bridges_count_vars) != 2).OnlyEnforceIf(b2.Not())
            self._model.AddBoolOr([b0, b2])
            for bridges in direction_bridges.values():
                self._model.Add(bridges >= 0)
                self._model.Add(bridges <= 1)

            connected_cells_count = self._input_grid[position]
            if connected_cells_count >= 0:
                self._model.Add(sum(bridges_count_vars) == 0)

                neighbor_positions = self._input_grid.neighbors_positions(position, "diagonal")
                neighbor_connected_cells = []
                for neighbor_position in neighbor_positions:
                    neighbor_bridge_vars = list(self._island_bridges_z3[neighbor_position].values())
                    b = self._model.NewBoolVar(f'nc_{neighbor_position}')
                    self._model.Add(sum(neighbor_bridge_vars) == 2).OnlyEnforceIf(b)
                    self._model.Add(sum(neighbor_bridge_vars) != 2).OnlyEnforceIf(b.Not())
                    neighbor_connected_cells.append(b)

                self._model.Add(sum(neighbor_connected_cells) == connected_cells_count)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(self._island_bridges_z3[island.position][direction] ==
                                     self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)
