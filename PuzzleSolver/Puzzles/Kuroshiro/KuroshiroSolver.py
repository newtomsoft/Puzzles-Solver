from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class KuroshiroSolver(GameSolver):
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
            [[Island(Position(r, c), 2) for c in range(self._input_grid.columns_number)] for r in range(self._input_grid.rows_number)]
        )

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
        self._add_links_constraints()

    def _add_initial_constraints(self):
        for position, direction_bridges in self._island_bridges_z3.items():
            bridges_count_vars = list(direction_bridges.values())
            input_value = self._input_grid[position]
            is_circle = input_value in ['□', '■']
            if is_circle:
                self._model.Add(sum(bridges_count_vars) == 2)
            else:
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

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(
                        self._island_bridges_z3[island.position][direction] ==
                        self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_links_constraints(self):
        for position, circle_value in [(position, value) for position, value in self._input_grid if value in ['□', '■']]:
            same_color_bools = self._same_color_circles_linked_boolvars(position, circle_value)
            other_color_bools = self._other_color_circles_linked_boolvars(position, circle_value)
            linked_circles_bools = same_color_bools + other_color_bools
            self._model.Add(sum(linked_circles_bools) == 2)

    def _same_color_circles_linked_boolvars(self, position: Position, circle_value: str) -> list:
        bool_vars = []
        for direction in Direction.orthogonal_directions():
            pairs = [(self._island_bridges_z3[position][direction], 1)]
            found = None
            current_position = position.after(direction)
            while current_position in self._island_bridges_z3:
                if (value := self._input_grid[current_position]) == circle_value:
                    found = value
                    break
                pairs.append((self._island_bridges_z3[current_position][direction], 1))
                current_position = current_position.after(direction)
            if found is None:
                continue

            eq_bools = []
            for i, (var, val) in enumerate(pairs):
                b = self._model.NewBoolVar(f'same_{position}_{direction}_{i}')
                self._model.Add(var == val).OnlyEnforceIf(b)
                self._model.Add(var != val).OnlyEnforceIf(b.Not())
                eq_bools.append(b)
            b_all = self._model.NewBoolVar(f'same_all_{position}_{direction}')
            for eb in eq_bools:
                self._model.AddImplication(b_all, eb)
            self._model.AddBoolOr([b_all] + [eb.Not() for eb in eq_bools])
            bool_vars.append(b_all)
        if not bool_vars:
            b_false = self._model.NewBoolVar(f'same_false_{position}')
            self._model.Add(b_false == 0)
            return [b_false]
        return bool_vars

    def _other_color_circles_linked_boolvars(self, circle_pos: Position, circle_value: str):
        bool_vars = []
        other_color = '■' if circle_value == '□' else '□'
        for other_circle_pos in [pos for pos, value in self._input_grid if value == other_color and pos.r != circle_pos.r and pos.c != circle_pos.c]:
            hor_turn_pos = Position(circle_pos.r, other_circle_pos.c)
            vert_turn_pos = Position(other_circle_pos.r, circle_pos.c)
            hor_direction = Direction.right() if other_circle_pos.c > circle_pos.c else Direction.left()
            vert_direction = Direction.down() if other_circle_pos.r > circle_pos.r else Direction.up()

            b_hor = self._to_other_circle_boolvar(circle_pos, other_circle_pos, hor_turn_pos, hor_direction, vert_direction, 'hor')
            b_vert = self._to_other_circle_boolvar(circle_pos, other_circle_pos, vert_turn_pos, vert_direction, hor_direction, 'vert')

            if b_hor is not None or b_vert is not None:
                b_or = self._model.NewBoolVar(f'other_{circle_pos}_{other_circle_pos}')
                alternatives = [b for b in [b_hor, b_vert] if b is not None]
                for alt in alternatives:
                    self._model.AddImplication(alt, b_or)
                self._model.AddBoolOr([b_or.Not()] + alternatives)
                bool_vars.append(b_or)

        return bool_vars

    def _to_other_circle_boolvar(self, circle_pos, other_circle_pos, turn_position, first_direction, second_direction, suffix: str):
        pairs = [(self._island_bridges_z3[circle_pos][first_direction], 1)]
        current_position = circle_pos.after(first_direction)
        while self._input_grid[current_position] == '' and current_position != turn_position:
            pairs.append((self._island_bridges_z3[current_position][first_direction], 1))
            current_position = current_position.after(first_direction)
        if self._input_grid[current_position] != '':
            return None

        pairs.append((self._island_bridges_z3[current_position][second_direction], 1))
        current_position = current_position.after(second_direction)
        while self._input_grid[current_position] == '' and current_position != other_circle_pos:
            pairs.append((self._island_bridges_z3[current_position][second_direction], 1))
            current_position = current_position.after(second_direction)
        if current_position != other_circle_pos:
            return None

        eq_bools = []
        for i, (var, val) in enumerate(pairs):
            b = self._model.NewBoolVar(f'other_{suffix}_{i}')
            self._model.Add(var == val).OnlyEnforceIf(b)
            self._model.Add(var != val).OnlyEnforceIf(b.Not())
            eq_bools.append(b)
        b_all = self._model.NewBoolVar(f'other_all_{suffix}')
        for eb in eq_bools:
            self._model.AddImplication(b_all, eb)
        self._model.AddBoolOr([b_all] + [eb.Not() for eb in eq_bools])
        return b_all
