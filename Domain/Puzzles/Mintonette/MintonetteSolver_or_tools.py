from collections import defaultdict, deque

from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class MintonetteSolver(GameSolver):
    Empty = None
    Unknown = -1

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._rows_number, self._columns_number = grid.rows_number, grid.columns_number
        self._turn_clues_by_positions: dict[Position, int | type(MintonetteSolver.Unknown)] = {
            position: turn_value for position, turn_value in self._input_grid if turn_value != self.Empty
        }

        self._positions_by_clues = defaultdict(list)
        for position, clue_path in self._turn_clues_by_positions.items():
            self._positions_by_clues[clue_path].append(position)

        self._paths_count = len(self._turn_clues_by_positions.values()) // 2

        self._island_grid: IslandGrid | None = None
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_ortools: Grid | None = None
        self._path_id_var_by_position = {}
        self._previous_solution: IslandGrid

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self._columns_number)] for r in range(self._rows_number)])

    def _init_solver(self):
        self._grid_ortools = Grid(
            [[{direction: self._model.NewBoolVar(f"{direction}_{r}-{c}") for direction in Direction.orthogonal_directions()} for c in range(self._columns_number)] for r in
             range(self._rows_number)])
        self._path_id_var_by_position = {position: self._model.NewIntVar(0, self._paths_count - 1, f"path_id_{position}") for position, _ in self._input_grid}
        self._is_turn_var_by_position = {}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._grid_ortools:
            self._init_solver()

        solution, _ = self._ensure_no_loop_solution()
        return solution

    def get_other_solution(self) -> IslandGrid:
        self._exclude_positions_values_together(self._previous_solution.get_positions())
        return self.get_solution()

    def _ensure_no_loop_solution(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._solver.Solve(self._model) in { cp_model.OPTIMAL, cp_model.FEASIBLE }:
            proposition_count += 1
            self._init_island_grid()
            for position, direction_bridges in self._grid_ortools:
                for direction, bridges in direction_bridges.items():
                    bridges_number = 1 if self._solver.Value(bridges) else 0
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_paths = self._island_grid.get_connected_positions()
            compliant = True
            for positions in connected_paths:
                if all(position not in self._turn_clues_by_positions for position in positions):
                    compliant = False
                    self._exclude_positions_values_together(positions)
            if compliant:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

        return IslandGrid.empty(), proposition_count

    def _exclude_positions_values_together(self, positions: set[Position]):
        no_clue_constraints = []
        for position in positions:
            for direction in Direction.orthogonal_directions():
                is_bridge = self._island_grid[position].direction_position_bridges.get(direction, [0, 0])[1] == 1
                var = self._grid_ortools[position][direction]
                if is_bridge:
                    no_clue_constraints.append(var)
                else:
                    no_clue_constraints.append(var.Not())

        self._model.AddBoolOr([c.Not() for c in no_clue_constraints])

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_opposite_constraints()
        self._add_bridges_sum_constraints()
        self._add_candidates_paths_constraints()

    def _add_initials_constraints(self):
        for position in self._grid_ortools.edge_up_positions():
            self._model.Add(self._grid_ortools[position][Direction.up()] == 0)
        for position in self._grid_ortools.edge_down_positions():
            self._model.Add(self._grid_ortools[position][Direction.down()] == 0)
        for position in self._grid_ortools.edge_left_positions():
            self._model.Add(self._grid_ortools[position][Direction.left()] == 0)
        for position in self._grid_ortools.edge_right_positions():
            self._model.Add(self._grid_ortools[position][Direction.right()] == 0)

        for position, island in [(position, island) for position, island in self._input_grid if type(island) is Island and not island.has_no_bridge()]:
            for direction, (_, bridges) in island.direction_position_bridges.items():
                self._model.Add(self._grid_ortools[position][direction] == (bridges == 1))

    def _add_opposite_constraints(self):
        for position, _ in self._grid_ortools:
            if position.up in self._grid_ortools:
                self._model.Add(self._grid_ortools[position][Direction.up()] == self._grid_ortools[position.up][Direction.down()])
            if position.down in self._grid_ortools:
                self._model.Add(self._grid_ortools[position][Direction.down()] == self._grid_ortools[position.down][Direction.up()])
            if position.left in self._grid_ortools:
                self._model.Add(self._grid_ortools[position][Direction.left()] == self._grid_ortools[position.left][Direction.right()])
            if position.right in self._grid_ortools:
                self._model.Add(self._grid_ortools[position][Direction.right()] == self._grid_ortools[position.right][Direction.left()])

    def _add_bridges_sum_constraints(self):
        for position, value in self._input_grid:
            if value == self.Empty:
                self._model.Add(sum([self._grid_ortools[position][direction] for direction in Direction.orthogonal_directions()]) == 2)
                continue
            self._model.Add(sum([self._grid_ortools[position][direction] for direction in Direction.orthogonal_directions()]) == 1)

    def _add_candidates_paths_constraints(self):
        for clue_position, _ in self._turn_clues_by_positions.items():
            paths_constraints = []
            for path in self._compute_candidates_paths(clue_position):
                path_active = self._model.NewBoolVar(f"path_active_{clue_position}_{len(paths_constraints)}")
                connects = []
                for index, current_position in enumerate(path[:-1]):
                    next_position = path[index + 1]
                    direction = current_position.direction_to(next_position)
                    connects.append(self._grid_ortools[current_position][direction])
                self._model.AddBoolAnd(connects).OnlyEnforceIf(path_active)
                paths_constraints.append(path_active)
            self._model.AddBoolOr(paths_constraints)

    def _compute_candidates_paths(self, start_node: Position) -> list[tuple]:
        value = self._input_grid[start_node]
        n_turn = value if value != self.Unknown else 8

        found_paths: list[tuple] = []
        queue = deque([(start_node, None, 0, [start_node])])
        visited_states = set()
        visited_states.add((start_node, None, 0))
        while queue:
            curr_pos, curr_dir, curr_turns, curr_path = queue.popleft()
            for direction in Direction.orthogonal_directions():
                next_pos = curr_pos.after(direction)

                if next_pos not in self._input_grid:
                    continue

                if next_pos in curr_path:
                    continue

                new_turns = curr_turns
                if curr_dir is not None and direction != curr_dir:
                    new_turns += 1

                if new_turns > n_turn:
                    continue

                new_path = curr_path + [next_pos]
                next_value = self._input_grid[next_pos]
                if value != self.Unknown:
                    if next_value == self.Empty:
                        queue.append((next_pos, direction, new_turns, new_path))
                        continue
                    if next_value in {self.Unknown, value} and new_turns == n_turn:
                        found_paths.append(tuple(new_path))
                        continue
                else:
                    if next_value == self.Empty:
                        queue.append((next_pos, direction, new_turns, new_path))
                        continue
                    if next_value == self.Unknown or next_value == new_turns:
                        found_paths.append(tuple(new_path))
                        continue

        return found_paths


