from typing import Dict

from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class SurizaSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_bridges: Dict[Position, Dict[Direction, cp_model.IntVar]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number + 1)] for r in range(self.input_grid.rows_number + 1)])

    def _init_solver(self):
        self._island_bridges = {island.position: {direction: self._model.new_int_var(0, 1, f"{island.position}_{direction}") for direction in Direction.orthogonals()} for island in self._island_grid.islands.values()}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._model.proto.constraints:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> (IslandGrid, int):
        proposition_count = 0
        status = self._solver.solve(self._model)
        while status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            proposition_count += 1
            for position, direction_bridges in self._island_bridges.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges:
                        continue
                    bridges_number = self._solver.value(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            for positions in connected_positions:
                not_all_equal = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        different = self._model.new_bool_var(f"diff{position}_{direction}")
                        self._model.add(self._island_bridges[position][direction] != value).only_enforce_if(different)
                        self._model.add(self._island_bridges[position][direction] == value).only_enforce_if(different.Not())
                        not_all_equal.append(different)

                self._model.AddBoolOr(not_all_equal)

            self._init_island_grid()
            status = self._solver.solve(self._model)

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        for island in self._previous_solution.islands.values():
            not_all_equal = []
            for direction, (position, value) in island.direction_position_bridges.items():
                different = self._model.new_bool_var(f"diff{position}_{direction}")
                self._model.add(self._island_bridges[position][direction] != value).only_enforce_if(different)
                self._model.add(self._island_bridges[position][direction] == value).only_enforce_if(different.Not())
                not_all_equal.append(different)

            self._model.AddBoolOr(not_all_equal)

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_numbers_constraints()

    def _add_initial_constraints(self):
        for col in range(self._island_grid.columns_number):
            self._model.add(self._island_bridges[Position(0, col)][Direction.up()] == 0)
            self._model.add(self._island_bridges[Position(self._island_grid.rows_number - 1, col)][Direction.down()] == 0)

        for row in range(self._island_grid.rows_number):
            self._model.add(self._island_bridges[Position(row, self._island_grid.columns_number - 1)][Direction.right()] == 0)
            self._model.add(self._island_bridges[Position(row, 0)][Direction.left()] == 0)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.add(self._island_bridges[island.position][direction] == self._island_bridges[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._model.add(self._island_bridges[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            bridge_sum = sum(self._island_bridges[island.position][direction] for direction in Direction.orthogonals())
            is_sum_0 = self._model.new_bool_var(f"is_sum_0_{island.position}")
            is_sum_2 = self._model.new_bool_var(f"is_sum_2_{island.position}")

            self._model.add_bool_or([is_sum_0, is_sum_2])
            self._model.add(bridge_sum == 0).only_enforce_if(is_sum_0)
            self._model.add(bridge_sum != 0).only_enforce_if(is_sum_0.Not())
            self._model.add(bridge_sum == 2).only_enforce_if(is_sum_2)
            self._model.add(bridge_sum != 2).only_enforce_if(is_sum_2.Not())

    def _add_numbers_constraints(self):
        for position, number in [(position, number) for position, number in self.input_grid if number != ' ']:
            up_left_corner = self._island_bridges[position][Direction.down()]
            down_left_corner = self._island_bridges[position.down][Direction.right()]
            down_right_corner = self._island_bridges[position.down_right][Direction.up()]
            up_right_corner = self._island_bridges[position.right][Direction.left()]
            self._model.add(up_left_corner + down_left_corner + down_right_corner + up_right_corner == number)
