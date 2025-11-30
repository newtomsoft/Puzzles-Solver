from collections import defaultdict, deque

from z3 import Solver, Not, And, sat, Bool, is_true, Int, Or

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class MintonetteSolver(GameSolver):
    horizontal = -1
    vertical = -2
    Empty = None
    Unknown = -1

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._rows_number, self._columns_number = grid.rows_number, grid.columns_number
        self._turn_clues_by_positions = {position: turn_value for position, turn_value in self._input_grid if turn_value != self.Empty}

        self._positions_by_clues = defaultdict(list)
        for position, clue_path in self._turn_clues_by_positions.items():
            self._positions_by_clues[clue_path].append(position)

        self._paths_count = len(self._turn_clues_by_positions.values()) // 2
        self._path_id_var_by_position = {position: Int(f"path_id_{position}") for position, _ in self._input_grid}
        self._path_id_var_by_position_hor = {position: Int(f"path_id_hor_{position}") for position, _ in self._input_grid}
        self._path_id_var_by_position_ver = {position: Int(f"path_id_ver_{position}") for position, _ in self._input_grid}
        self._island_grid: IslandGrid | None = None
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: IslandGrid

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self._columns_number)] for r in range(self._rows_number)])

    def _init_solver(self):
        self._grid_z3 = Grid(
            [[{direction: Bool(f"{r}-{c}-{direction}") for direction in Direction.orthogonal_directions()} for c in range(self._columns_number)] for r in
             range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution = self._compute_solution()
        return solution

    def get_other_solution(self):
        self._exclude_positions_values_together(self._previous_solution.get_positions())
        return self.get_solution()

    def _compute_solution(self) -> IslandGrid:
        propositions_count = 0
        if self._solver.check() != sat:
            return IslandGrid.empty()

        self._init_island_grid()
        model = self._solver.model()
        propositions_count += 1
        for position, direction_bridges in self._grid_z3:
            for direction, bridges in direction_bridges.items():
                bridges_number = 1 if is_true(model.eval(bridges)) else 0
                if bridges_number > 0:
                    self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                    self._island_grid[position].direction_position_bridges.pop(direction)
            self._island_grid[position].set_bridges_count_according_to_directions_bridges()

        self._previous_solution = self._island_grid
        return self._island_grid

    def _exclude_positions_values_together(self, positions: set[Position]):
        no_clue_constraints = []
        for position in positions:
            no_clue_constraints += [
                self._grid_z3[position][direction] == (self._island_grid[position].direction_position_bridges.get(direction, [0, 0])[1] == 1) for
                direction in Direction.orthogonal_directions()
            ]
        self._solver.add(Not(And(no_clue_constraints)))

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_opposite_constraints()
        self._add_bridges_sum_constraints()
        self._add_candidates_paths_constraints()

    def _add_initials_constraints(self):
        for position in self._grid_z3.edge_up_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.up()]))
        for position in self._grid_z3.edge_down_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.down()]))
        for position in self._grid_z3.edge_left_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.left()]))
        for position in self._grid_z3.edge_right_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.right()]))

        for position, island in [(position, island) for position, island in self._input_grid if type(island) is Island and not island.has_no_bridge()]:
            for direction, (_, bridges) in island.direction_position_bridges.items():
                self._solver.add(self._grid_z3[position][direction] == (bridges == 1))

    def _add_opposite_constraints(self):
        for position, _ in self._grid_z3:
            if position.up in self._grid_z3:
                self._solver.add(self._grid_z3[position][Direction.up()] == self._grid_z3[position.up][Direction.down()])
            if position.down in self._grid_z3:
                self._solver.add(self._grid_z3[position][Direction.down()] == self._grid_z3[position.down][Direction.up()])
            if position.left in self._grid_z3:
                self._solver.add(self._grid_z3[position][Direction.left()] == self._grid_z3[position.left][Direction.right()])
            if position.right in self._grid_z3:
                self._solver.add(self._grid_z3[position][Direction.right()] == self._grid_z3[position.right][Direction.left()])

    def _add_bridges_sum_constraints(self):
        for position, value in self._input_grid:
            if value == self.Empty:
                self._solver.add(sum([self._grid_z3[position][direction] for direction in Direction.orthogonal_directions()]) == 2)
                continue
            self._solver.add(sum([self._grid_z3[position][direction] for direction in Direction.orthogonal_directions()]) == 1)

    def _add_candidates_paths_constraints(self):
        for clue_position, _ in self._turn_clues_by_positions.items():
            paths_constraints = []
            for path in self._compute_candidates_paths(clue_position):
                connects = []
                for index, current_position in enumerate(path[:-1]):
                    next_position = path[index + 1]
                    direction = current_position.direction_to(next_position)
                    connects.append(self._grid_z3[current_position][direction])
                paths_constraints.append(And(connects))
            self._solver.add(Or(paths_constraints))

    def _compute_candidates_paths(self, start_node: Position) -> list[tuple]:
        value = self._input_grid[start_node]
        n_turn = value if value != self.Unknown else self._rows_number * self._columns_number

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
