from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position


class WamazuSolver:
    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._connections_number = sum(1 for row in grid for cell in row if cell == 1) // 2
        self._island_grid: IslandGrid | None = None
        self._rows_number = self._input_grid.rows_number
        self._columns_number = self._input_grid.columns_number
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._cp_solver = cp_model.CpSolver()
        self._island_bridges_z3: dict[Position, dict[Direction, cp_model.IntVar]] = {}
        self._previous_solution: IslandGrid | None = None
        self._solver_initialized = False

    def _init_island_grid(self):
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

        solution, _ = self._ensure_no_loop()
        return solution

    def _ensure_no_loop(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._cp_solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = self._cp_solver.Value(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(
                            self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[
                        position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            loop_positions = self._island_grid.get_loop_positions()
            if len(loop_positions) == 0:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            eq_bools = []
            for island in [self._island_grid.islands[position] for position in loop_positions]:
                for direction, (_, value) in island.direction_position_bridges.items():
                    b = self._model.NewBoolVar(f'loop_eq_{island.position}_{direction}')
                    var = self._island_bridges_z3[island.position][direction]
                    self._model.Add(var == value).OnlyEnforceIf(b)
                    self._model.Add(var != value).OnlyEnforceIf(b.Not())
                    eq_bools.append(b)
            self._model.Add(sum(eq_bools) <= len(eq_bools) - 1)
            self._init_island_grid()

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

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_circles_constraints()
        self._add_turns_constraints()
        self._add_opposite_bridges_constraints()

    def _add_circles_constraints(self):
        for position in [position for position, value in self._input_grid if value == 1]:
            bridges = self._island_bridges_z3[position]
            bridges_count_vars = list(bridges.values())
            self._model.Add(sum(bridges_count_vars) == 1)
            for direction_bridges in bridges.values():
                self._model.Add(direction_bridges >= 0)
                self._model.Add(direction_bridges <= 1)

    def _add_turns_constraints(self):
        turn_patterns = [
            ([Direction.left(), Direction.up()], [Direction.right(), Direction.down()]),
            ([Direction.right(), Direction.down()], [Direction.left(), Direction.up()]),
            ([Direction.up(), Direction.right()], [Direction.down(), Direction.left()]),
            ([Direction.down(), Direction.left()], [Direction.up(), Direction.right()]),
        ]
        for position in [position for position, value in self._input_grid if value != 1]:
            bridges = self._island_bridges_z3[position]
            alt_bools = []
            for idx, (dirs_true, dirs_false) in enumerate(turn_patterns):
                eq_bools = []
                for d in dirs_true:
                    b = self._model.NewBoolVar(f'turn_{position}_t_{idx}_{d}')
                    self._model.Add(bridges[d] == 1).OnlyEnforceIf(b)
                    self._model.Add(bridges[d] != 1).OnlyEnforceIf(b.Not())
                    eq_bools.append(b)
                for d in dirs_false:
                    b = self._model.NewBoolVar(f'turn_{position}_f_{idx}_{d}')
                    self._model.Add(bridges[d] == 0).OnlyEnforceIf(b)
                    self._model.Add(bridges[d] != 0).OnlyEnforceIf(b.Not())
                    eq_bools.append(b)
                b_all = self._model.NewBoolVar(f'turn_{position}_alt_{idx}')
                for eb in eq_bools:
                    self._model.AddImplication(b_all, eb)
                self._model.AddBoolOr([b_all] + [eb.Not() for eb in eq_bools])
                alt_bools.append(b_all)
            self._model.AddBoolOr(alt_bools)
            for direction_bridges in bridges.values():
                self._model.Add(direction_bridges >= 0)
                self._model.Add(direction_bridges <= 1)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(self._island_bridges_z3[island.position][direction] ==
                                     self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)
