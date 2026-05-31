from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class RimotoejjiSolver(GameSolver):
    no_clue = ' '

    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._N = grid.rows_number
        self._V = self._N + 1
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_grid: IslandGrid | None = None
        self._edge: dict[Position, dict[Direction, cp_model.IntVar]] = {}
        self._inside: dict[Position, cp_model.IntVar] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self._V)] for r in range(self._V)])

    def _init_variables(self):
        for pos in self._island_grid.islands:
            self._edge[pos] = {d: self._model.new_bool_var(f"e_{pos}_{d}") for d in Direction.orthogonal_directions()}
        for r in range(self._N):
            for c in range(self._N):
                self._inside[Position(r, c)] = self._model.new_bool_var(f"inside_{r}_{c}")

    def _init_solver(self):
        self._init_island_grid()
        self._init_variables()
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._model.proto.constraints:
            self._init_solver()
        solution, _ = self._ensure_all_islands_connected()
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return Grid.empty()
        literals = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                if value == 1:
                    literals.append(self._edge[island.position][direction])
        if literals:
            self._model.add_bool_or([lit.negated() for lit in literals])
        return self.get_solution()

    def _add_constraints(self):
        self._add_border_constraints()
        self._add_opposite_bridge_constraints()
        self._add_degree_constraints()
        self._add_inside_parity_constraints()
        self._add_clues_inside_constraints()
        self._add_clues_direction_constraints()

    def _add_border_constraints(self):
        for c in range(self._V):
            self._model.add(self._edge[Position(0, c)][Direction.up()] == 0)
            self._model.add(self._edge[Position(self._V - 1, c)][Direction.down()] == 0)
        for r in range(self._V):
            self._model.add(self._edge[Position(r, 0)][Direction.left()] == 0)
            self._model.add(self._edge[Position(r, self._V - 1)][Direction.right()] == 0)

    def _add_opposite_bridge_constraints(self):
        for pos in self._island_grid.islands:
            for direction in Direction.orthogonal_directions():
                neighbor_pos = pos.after(direction)
                if neighbor_pos in self._island_grid:
                    self._model.add(self._edge[pos][direction] == self._edge[neighbor_pos][direction.opposite])
                else:
                    self._model.add(self._edge[pos][direction] == 0)

    def _add_degree_constraints(self):
        for pos in self._island_grid.islands:
            vars_list = [self._edge[pos][d] for d in Direction.orthogonal_directions()]
            total = self._model.new_int_var(0, 4, f"deg_sum_{pos}")
            self._model.add(total == sum(vars_list))
            self._model.add(total == 2)

    def _add_inside_parity_constraints(self):
        for r in range(self._N):
            v_edge_r_0 = self._edge[Position(r, 0)][Direction.down()]
            self._model.add(self._inside[Position(r, 0)] == v_edge_r_0)
            for c in range(1, self._N):
                a = self._inside[Position(r, c - 1)]
                b = self._edge[Position(r, c)][Direction.down()]
                z = self._inside[Position(r, c)]
                self._model.add(z >= a - b)
                self._model.add(z >= b - a)
                self._model.add(z <= a + b)
                self._model.add(z <= 2 - a - b)

    def _add_clues_inside_constraints(self):
        for pos, val in self.input_grid:
            if val != ' ':
                self._model.add(self._inside[pos] == 1)

    @staticmethod
    def _encode_longest_chain_length(model: cp_model.CpModel, inside_vars: list[cp_model.IntVar], prefix: str) -> tuple[cp_model.IntVar, list[cp_model.IntVar]]:
        k = len(inside_vars)
        chain = []
        for i in range(k):
            chain_var = model.new_bool_var(f"{prefix}_chain_{i}")
            if i == 0:
                model.add(chain_var == inside_vars[0])
            else:
                model.add_multiplication_equality(chain_var, [chain[i - 1], inside_vars[i]])
            chain.append(chain_var)
        length_var = model.new_int_var(0, k, f"{prefix}_len")
        model.add(length_var == sum(chain))
        return length_var, chain

    @staticmethod
    def _add_gt(model: cp_model.CpModel, a: cp_model.IntVar, b: cp_model.IntVar):
        model.add(a >= b + 1)

    def _add_clues_direction_constraints(self):
        for pos, val in self.input_grid:
            if val == ' ':
                continue
            r, c = pos.r, pos.c
            up_vars = [self._inside[Position(r - k - 1, c)] for k in range(r)]
            down_vars = [self._inside[Position(r + k + 1, c)] for k in range(self._N - r - 1)]
            left_vars = [self._inside[Position(r, c - k - 1)] for k in range(c)]
            right_vars = [self._inside[Position(r, c + k + 1)] for k in range(self._N - c - 1)]
            up_len, _ = self._encode_longest_chain_length(self._model, up_vars, f"len_up_{r}_{c}")
            down_len, _ = self._encode_longest_chain_length(self._model, down_vars, f"len_down_{r}_{c}")
            left_len, _ = self._encode_longest_chain_length(self._model, left_vars, f"len_left_{r}_{c}")
            right_len, _ = self._encode_longest_chain_length(self._model, right_vars, f"len_right_{r}_{c}")
            if val == '↓':
                self._add_gt(self._model, down_len, up_len)
                self._add_gt(self._model, down_len, left_len)
                self._add_gt(self._model, down_len, right_len)
            elif val == '↑':
                self._add_gt(self._model, up_len, down_len)
                self._add_gt(self._model, up_len, left_len)
                self._add_gt(self._model, up_len, right_len)
            elif val == '→':
                self._add_gt(self._model, right_len, left_len)
                self._add_gt(self._model, right_len, up_len)
                self._add_gt(self._model, right_len, down_len)
            elif val == '←':
                self._add_gt(self._model, left_len, right_len)
                self._add_gt(self._model, left_len, up_len)
                self._add_gt(self._model, left_len, down_len)
            elif val == '+':
                max_len = self._model.new_int_var(0, self._N, f"max_len_{r}_{c}")
                self._model.add_max_equality(max_len, [up_len, down_len, left_len, right_len])
                is_max_vars = []
                for dir_len, suffix in [(up_len, 'up'), (down_len, 'down'), (left_len, 'left'), (right_len, 'right')]:
                    is_max = self._model.new_bool_var(f"ismax_{r}_{c}_{suffix}")
                    diff = self._model.new_int_var(0, self._N, f"diff_{r}_{c}_{suffix}")
                    self._model.add(diff == max_len - dir_len)
                    self._model.add(diff <= self._N * (1 - is_max))
                    self._model.add(diff >= 1 - (self._N + 1) * is_max)
                    is_max_vars.append(is_max)
                n_max = self._model.new_int_var(0, 4, f"n_max_{r}_{c}")
                self._model.add(n_max == sum(is_max_vars))
                self._model.add(n_max >= 2)
                self._model.add(max_len >= 1)

    def _extract_solution_to_island_grid(self):
        self._init_island_grid()
        for pos, direction_vars in self._edge.items():
            for direction, var in direction_vars.items():
                if direction not in self._island_grid[pos].direction_position_bridges:
                    continue
                if self._solver.value(var) > 0:
                    neighbor_pos = self._island_grid[pos].direction_position_bridges[direction][0]
                    self._island_grid[pos].set_bridge_to_position(neighbor_pos, 1)
                else:
                    if direction in self._island_grid[pos].direction_position_bridges:
                        self._island_grid[pos].direction_position_bridges.pop(direction)
            self._island_grid[pos].set_bridges_count_according_to_directions_bridges()

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        status = self._solver.solve(self._model)
        while status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            proposition_count += 1
            self._extract_solution_to_island_grid()
            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) <= 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count
            for positions in connected_positions:
                literals = []
                for pos in positions:
                    for direction, (_, value) in self._island_grid[pos].direction_position_bridges.items():
                        if value == 1:
                            literals.append(self._edge[pos][direction])
                if literals:
                    self._model.add_bool_or([lit.negated() for lit in literals])
            status = self._solver.solve(self._model)
        return IslandGrid.empty(), proposition_count
