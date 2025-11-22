from collections import Counter

from z3 import Solver, Not, And, Or, sat, Bool, is_true, Sum, Int, Implies

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KanjoSolver(GameSolver):
    horizontal = -1
    vertical = -2
    empty = None

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._rows_number, self._columns_number = grid.rows_number, grid.columns_number
        self._clues_by_positions = {position: clue_loop for position, clue_loop in self._input_grid if type(clue_loop) is int}
        self._loop_count = len(Counter(self._clues_by_positions.values()))
        self._loop_id_var_by_position = {position: Int(f"loop_id_{position}") for position, _ in self._input_grid}
        self._loop_id_var_by_position_hor = {position: Int(f"loop_id_hor_{position}") for position, _ in self._input_grid}
        self._loop_id_var_by_position_ver = {position: Int(f"loop_id_ver_{position}") for position, _ in self._input_grid}
        self._island_grid: IslandGrid | None = None
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: IslandGrid

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self._columns_number)] for r in range(self._rows_number)])

    def _init_solver(self):
        self._grid_z3 = Grid(
            [[{direction: Bool(f"{direction}_{r}-{c}") for direction in Direction.orthogonal_directions()} for c in range(self._columns_number)] for r in
             range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_islands_grouped()
        return solution

    def _ensure_all_islands_grouped(self) -> tuple[IslandGrid, int]:
        propositions_count = 0
        while self._solver.check() == sat:
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

            connected_positions = self._island_grid.get_linear_connected_positions(exclude_without_bridge=False)
            if len(connected_positions) == self._loop_count:
                self._previous_solution = self._island_grid
                return self._island_grid, propositions_count

            # todo optimize adding constraints
            constraints = []
            for position, island in self._island_grid:
                constraints += [self._grid_z3[position][direction] == (island.direction_position_bridges.get(direction, [0, 0])[1] == 1) for direction in
                                Direction.orthogonal_directions()]
            self._solver.add(Not(And(constraints)))

        return IslandGrid.empty(), propositions_count

    def get_other_solution(self):
        constraints = []
        for position, island in self._previous_solution:
            constraints += [self._grid_z3[position][direction] == (island.direction_position_bridges.get(direction, [0, 0])[1] == 1) for direction in
                            Direction.orthogonal_directions()]
        self._solver.add(Not(And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_opposite_constraints()
        self._add_bridges_sum_constraints()
        self._add_one_way_by_clues_constraints()
        self._add_one_loop_for_same_clues_constraints()

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
        for position, _ in self._grid_z3:
            sum_constraint_2 = sum([self._grid_z3[position][direction] for direction in Direction.orthogonal_directions()]) == 2
            sum_constraint_4 = sum([self._grid_z3[position][direction] for direction in Direction.orthogonal_directions()]) == 4
            self._solver.add(Or(sum_constraint_2, sum_constraint_4))

    def _add_one_way_by_clues_constraints(self):
        for position, loop_id in self._clues_by_positions.items():
            self._add_one_way_clue_constraints(position)

    def _add_one_way_clue_constraints(self, position: Position):
        sum_constraint = Sum([self._grid_z3[position][direction] for direction in Direction.orthogonal_directions()]) == 2
        self._solver.add(sum_constraint)

    def _add_one_loop_for_same_clues_constraints(self):
        for position, loop_id in self._clues_by_positions.items():
            self._solver.add(self._loop_id_var_by_position[position] == loop_id)

        for position, _ in self._grid_z3:
            for direction in Direction.orthogonal_directions():
                self._add_one_loop_for_same_clues_constraints_step_position(position, direction)

    def _add_one_loop_for_same_clues_constraints_step_position(self, position, direction: Direction):
        next_position = position.after(direction)
        if next_position not in self._grid_z3:
            return

        position_single_way = sum([self._grid_z3[position][direction] for direction in Direction.orthogonal_directions()]) == 2
        position_multi_way = sum([self._grid_z3[position][direction] for direction in Direction.orthogonal_directions()]) == 4
        next_position_single_way = sum([self._grid_z3[next_position][direction] for direction in Direction.orthogonal_directions()]) == 2
        next_position_multi_way = sum([self._grid_z3[next_position][direction] for direction in Direction.orthogonal_directions()]) == 4

        self._add_single_to_single_constraint(position, direction, next_position, position_single_way, next_position_single_way)
        self._add_multi_to_single_constraint(position, direction, next_position, next_position_single_way, position_multi_way)
        self._add_single_to_multi_constraint(position, direction, next_position, next_position_multi_way, position_single_way)
        self._add_multi_to_multi_constraint(position, direction, next_position, position_multi_way, next_position_multi_way)

    def _add_single_to_single_constraint(self, position, direction: Direction, next_position, position_single_way: bool, next_position_single_way: bool):
        single_single_equality = self._loop_id_var_by_position[position] == self._loop_id_var_by_position[next_position]
        self._solver.add(
            Implies(
                And(position_single_way, next_position_single_way, self._grid_z3[position][direction]),
                single_single_equality
            ))

    def _add_multi_to_single_constraint(self, position, direction: Direction, next_position, next_position_single_way: bool, position_multi_way: bool):
        if direction in [Direction.left(), Direction.right()]:
            multi_single_equality = self._loop_id_var_by_position_hor[position] == self._loop_id_var_by_position[next_position]
        else:
            multi_single_equality = self._loop_id_var_by_position_ver[position] == self._loop_id_var_by_position[next_position]
        self._solver.add(
            Implies(
                And(position_multi_way, next_position_single_way),
                multi_single_equality
            ))

    def _add_single_to_multi_constraint(self, position, direction: Direction, next_position, next_position_multi_way: bool, position_single_way: bool):
        if direction in [Direction.left(), Direction.right()]:
            single_multi_equality = self._loop_id_var_by_position_hor[next_position] == self._loop_id_var_by_position[position]
        else:
            single_multi_equality = self._loop_id_var_by_position_ver[next_position] == self._loop_id_var_by_position[position]
        self._solver.add(
            Implies(
                And(position_single_way, next_position_multi_way, self._grid_z3[position][direction]),
                Or(And(single_multi_equality, next_position_multi_way),
                   self._loop_id_var_by_position[position] == self._loop_id_var_by_position[next_position])
            ))

    def _add_multi_to_multi_constraint(self, position, direction: Direction, next_position, position_multi_way: bool, next_position_multi_way: bool):
        if direction in [Direction.left(), Direction.right()]:
            multi_multi_equality = self._loop_id_var_by_position_hor[position] == self._loop_id_var_by_position_hor[next_position]
        else:
            multi_multi_equality = self._loop_id_var_by_position_ver[position] == self._loop_id_var_by_position_ver[next_position]
        self._solver.add(
            Implies(
                And(position_multi_way, next_position_multi_way),
                multi_multi_equality
            ))
