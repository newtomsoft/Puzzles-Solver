from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

class MidLoopSolver(GameSolver):
    def __init__(self, input_grid: Grid):
        self.rows_number = (input_grid.rows_number + 1) // 2
        self.columns_number = (input_grid.columns_number + 1) // 2
        self.dots_positions = []
        for position, value in input_grid:
            if value:
                self.dots_positions.append(Position(position.r / 2, position.c / 2))

        self._input_grid = Grid([[0 for _ in range(self.columns_number)] for _ in range(self.rows_number)])
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._model = cp_model.CpModel()
        self._cp_solver = cp_model.CpSolver()
        self._island_bridges_z3: dict[Position, dict[Direction, cp_model.IntVar]] = {}
        self._previous_solution: IslandGrid | None = None
        self._solver_initialized = False

    def init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self.columns_number)] for r in range(self.rows_number)]
        )

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {
                direction: self._model.NewIntVar(0, 1, f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()
            }
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
        while self._cp_solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = self._cp_solver.Value(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(
                            self._island_grid[position].direction_position_bridges[direction][0], bridges_number
                        )
                    elif (
                            position in self._island_grid
                            and direction in self._island_grid[position].direction_position_bridges
                    ):
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
        self._add_minimal_edge_segments_constraints()
        self._add_minimal_inside_segments_constraints()
        self._add_symmetry_constraints()
        self._add_opposite_bridges_constraints()

    def _pairs_to_boolvar(self, pairs, name: str):
        eq_bools = []
        for i, (var, val) in enumerate(pairs):
            b = self._model.NewBoolVar(f'{name}_eq_{i}')
            self._model.Add(var == val).OnlyEnforceIf(b)
            self._model.Add(var != val).OnlyEnforceIf(b.Not())
            eq_bools.append(b)
        b_all = self._model.NewBoolVar(f'{name}_all')
        for eb in eq_bools:
            self._model.AddImplication(b_all, eb)
        self._model.AddBoolOr([b_all] + [eb.Not() for eb in eq_bools])
        return b_all

    def _add_initial_constraints(self):
        for position, directions_bridges in self._island_bridges_z3.items():
            bridges_count_vars = list(directions_bridges.values())
            b0 = self._model.NewBoolVar(f'sum0_{position}')
            b2 = self._model.NewBoolVar(f'sum2_{position}')
            self._model.Add(sum(bridges_count_vars) == 0).OnlyEnforceIf(b0)
            self._model.Add(sum(bridges_count_vars) != 0).OnlyEnforceIf(b0.Not())
            self._model.Add(sum(bridges_count_vars) == 2).OnlyEnforceIf(b2)
            self._model.Add(sum(bridges_count_vars) != 2).OnlyEnforceIf(b2.Not())
            self._model.AddBoolOr([b0, b2])
            for direction_bridges in directions_bridges.values():
                self._model.Add(direction_bridges >= 0)
                self._model.Add(direction_bridges <= 1)

    def _add_minimal_edge_segments_constraints(self):
        for dot_position in [
            position
            for position in self.dots_positions
            if self._input_grid.is_position_in_edge_up(position) or self._input_grid.is_position_in_edge_down(position)
        ]:
            self._add_minimal_horizontal_segments_constraints(dot_position)
        for dot_position in [
            position
            for position in self.dots_positions
            if self._input_grid.is_position_in_edge_left(position)
               or self._input_grid.is_position_in_edge_right(position)
        ]:
            self._add_minimal_vertical_segments_constraints(dot_position)

    def _add_minimal_inside_segments_constraints(self):
        for dot_position in [
            position
            for position in self.dots_positions
            if not self._input_grid.is_position_in_edge_up(position)
               and not self._input_grid.is_position_in_edge_down(position)
               and not self._input_grid.is_position_in_edge_left(position)
               and not self._input_grid.is_position_in_edge_right(position)
        ]:
            self._add_minimal_segment_constraints(dot_position)

    def _add_minimal_segment_constraints(self, dot_position: Position):
        b_horiz = self._minimal_horizontal_segments_boolvar(dot_position)
        b_vert = self._minimal_vertical_segments_boolvar(dot_position)
        alternatives = [b for b in [b_horiz, b_vert] if b is not None]
        if alternatives:
            self._model.AddBoolOr(alternatives)

    def _add_minimal_horizontal_segments_constraints(self, dot_position: Position):
        b = self._minimal_horizontal_segments_boolvar(dot_position)
        if b is not None:
            self._model.Add(b == 1)

    def _minimal_horizontal_segments_boolvar(self, dot_position: Position):
        if not dot_position.is_on_row():
            return None

        if not dot_position.is_on_column():
            position_left = Position(dot_position.r, int(dot_position.c))
            position_right = position_left.right
            pairs = [
                (self._island_bridges_z3[position_left][Direction.right()], 1),
                (self._island_bridges_z3[position_right][Direction.left()], 1),
            ]
            return self._pairs_to_boolvar(pairs, f'min_h_{dot_position}')

        pairs = [
            (self._island_bridges_z3[dot_position][Direction.left()], 1),
            (self._island_bridges_z3[dot_position][Direction.right()], 1),
            (self._island_bridges_z3[dot_position][Direction.up()], 0),
            (self._island_bridges_z3[dot_position][Direction.down()], 0),
        ]
        return self._pairs_to_boolvar(pairs, f'min_h_cross_{dot_position}')

    def _add_minimal_vertical_segments_constraints(self, dot_position: Position):
        b = self._minimal_vertical_segments_boolvar(dot_position)
        if b is not None:
            self._model.Add(b == 1)

    def _minimal_vertical_segments_boolvar(self, dot_position: Position):
        if not dot_position.is_on_column():
            return None

        if not dot_position.is_on_row():
            position_up = Position(int(dot_position.r), dot_position.c)
            position_down = position_up.down
            pairs = [
                (self._island_bridges_z3[position_up][Direction.down()], 1),
                (self._island_bridges_z3[position_down][Direction.up()], 1),
            ]
            return self._pairs_to_boolvar(pairs, f'min_v_{dot_position}')

        pairs = [
            (self._island_bridges_z3[dot_position][Direction.up()], 1),
            (self._island_bridges_z3[dot_position][Direction.down()], 1),
            (self._island_bridges_z3[dot_position][Direction.left()], 0),
            (self._island_bridges_z3[dot_position][Direction.right()], 0),
        ]
        return self._pairs_to_boolvar(pairs, f'min_v_cross_{dot_position}')

    def _add_symmetry_constraints(self):
        for dot_position in self.dots_positions:
            if not dot_position.is_on_row():
                self._add_must_symetry_vertical_segment_constraint(dot_position)
            if not dot_position.is_on_column():
                self._add_must_symetry_horizontal_segment_constraint(dot_position)
            if dot_position.is_on_row() and dot_position.is_on_column():
                self._add_symetry_segment_constraint(dot_position)

    def _add_must_symetry_vertical_segment_constraint(self, dot_position: Position):
        b = self._symetry_vertical_segment_boolvar(dot_position)
        if b is not None:
            self._model.Add(b == 1)

    def _add_must_symetry_horizontal_segment_constraint(self, dot_position: Position):
        b = self._symetry_horizontal_segment_boolvar(dot_position)
        if b is not None:
            self._model.Add(b == 1)

    def _add_symetry_segment_constraint(self, dot_position: Position):
        b_vert = self._symetry_vertical_segment_boolvar(dot_position)
        b_horiz = self._symetry_horizontal_segment_boolvar(dot_position)
        alternatives = [b for b in [b_vert, b_horiz] if b is not None]
        if alternatives:
            self._model.AddBoolOr(alternatives)

    def _symetry_vertical_segment_boolvar(self, dot_position: Position):
        if self._input_grid.is_position_in_edge_up(dot_position) or self._input_grid.is_position_in_edge_down(
                dot_position
        ):
            return None

        all_sub_bools = []

        if dot_position.is_on_row():
            for direction in [Direction.up(), Direction.down()]:
                pairs = [(self._island_bridges_z3[dot_position][direction], 1)]
                b = self._pairs_to_boolvar(pairs, f'sym_v_onrow_{dot_position}_{direction}')
                all_sub_bools.append(b)

            position_up = dot_position.up
            position_down = dot_position.down
            prev_cumul = None
            idx = 0
            while position_up in self._input_grid and position_down in self._input_grid:
                b_ugd = self._pairs_to_boolvar(
                    [(self._island_bridges_z3[position_up][Direction.down()], 1)],
                    f'sym_v_pair_{idx}_ugd'
                )
                b_dgu = self._pairs_to_boolvar(
                    [(self._island_bridges_z3[position_down][Direction.up()], 1)],
                    f'sym_v_pair_{idx}_dgu'
                )

                b_cumul = self._model.NewBoolVar(f'sym_v_cumul_{idx}')
                if prev_cumul is None:
                    self._model.AddImplication(b_cumul, b_ugd)
                    self._model.AddImplication(b_cumul, b_dgu)
                    self._model.AddBoolOr([b_cumul, b_ugd.Not(), b_dgu.Not()])
                else:
                    self._model.AddImplication(b_cumul, prev_cumul)
                    self._model.AddImplication(b_cumul, b_ugd)
                    self._model.AddImplication(b_cumul, b_dgu)
                    self._model.AddBoolOr([b_cumul, prev_cumul.Not(), b_ugd.Not(), b_dgu.Not()])

                b_eq_extend = self._model.NewBoolVar(f'sym_v_ext_{idx}')
                var_up = self._island_bridges_z3[position_up][Direction.up()]
                var_down = self._island_bridges_z3[position_down][Direction.down()]
                self._model.Add(var_up == var_down).OnlyEnforceIf(b_eq_extend)
                self._model.Add(var_up != var_down).OnlyEnforceIf(b_eq_extend.Not())

                b_impl = self._model.NewBoolVar(f'sym_v_impl_{idx}')
                self._model.AddBoolOr([b_impl.Not(), b_cumul.Not(), b_eq_extend])
                self._model.AddBoolOr([b_cumul, b_impl])
                self._model.AddBoolOr([b_eq_extend.Not(), b_impl])

                all_sub_bools.append(b_impl)

                prev_cumul = b_cumul
                position_up = position_up.up
                position_down = position_down.down
                idx += 1
        else:
            position_up = Position(int(dot_position.r), dot_position.c)
            position_down = position_up.down
            pairs = [
                (self._island_bridges_z3[position_up][Direction.down()], 1),
                (self._island_bridges_z3[position_down][Direction.up()], 1),
            ]
            b = self._pairs_to_boolvar(pairs, f'sym_v_base_{dot_position}')
            all_sub_bools.append(b)

            prev_cumul = b
            idx = 0
            while position_up in self._input_grid and position_down in self._input_grid:
                b_ugd = self._pairs_to_boolvar(
                    [(self._island_bridges_z3[position_up][Direction.down()], 1)],
                    f'sym_v_pair_{idx}_ugd'
                )
                b_dgu = self._pairs_to_boolvar(
                    [(self._island_bridges_z3[position_down][Direction.up()], 1)],
                    f'sym_v_pair_{idx}_dgu'
                )

                b_cumul = self._model.NewBoolVar(f'sym_v_cumul_{idx}')
                self._model.AddImplication(b_cumul, prev_cumul)
                self._model.AddImplication(b_cumul, b_ugd)
                self._model.AddImplication(b_cumul, b_dgu)
                self._model.AddBoolOr([b_cumul, prev_cumul.Not(), b_ugd.Not(), b_dgu.Not()])

                b_eq_extend = self._model.NewBoolVar(f'sym_v_ext_{idx}')
                var_up = self._island_bridges_z3[position_up][Direction.up()]
                var_down = self._island_bridges_z3[position_down][Direction.down()]
                self._model.Add(var_up == var_down).OnlyEnforceIf(b_eq_extend)
                self._model.Add(var_up != var_down).OnlyEnforceIf(b_eq_extend.Not())

                b_impl = self._model.NewBoolVar(f'sym_v_impl_{idx}')
                self._model.AddBoolOr([b_impl.Not(), b_cumul.Not(), b_eq_extend])
                self._model.AddBoolOr([b_cumul, b_impl])
                self._model.AddBoolOr([b_eq_extend.Not(), b_impl])

                all_sub_bools.append(b_impl)

                prev_cumul = b_cumul
                position_up = position_up.up
                position_down = position_down.down
                idx += 1

        if not all_sub_bools:
            return None
        b_block = self._model.NewBoolVar(f'sym_v_block_{dot_position}')
        for b_sub in all_sub_bools:
            self._model.AddImplication(b_block, b_sub)
        return b_block

    def _symetry_horizontal_segment_boolvar(self, dot_position: Position):
        if self._input_grid.is_position_in_edge_left(dot_position) or self._input_grid.is_position_in_edge_right(
                dot_position
        ):
            return None

        all_sub_bools = []

        if dot_position.is_on_column():
            for direction in [Direction.left(), Direction.right()]:
                pairs = [(self._island_bridges_z3[dot_position][direction], 1)]
                b = self._pairs_to_boolvar(pairs, f'sym_h_oncol_{dot_position}_{direction}')
                all_sub_bools.append(b)

            position_left = dot_position.left
            position_right = dot_position.right
            prev_cumul = None
            idx = 0
            while position_left in self._input_grid and position_right in self._input_grid:
                b_lgr = self._pairs_to_boolvar(
                    [(self._island_bridges_z3[position_left][Direction.right()], 1)],
                    f'sym_h_pair_{idx}_lgr'
                )
                b_rgl = self._pairs_to_boolvar(
                    [(self._island_bridges_z3[position_right][Direction.left()], 1)],
                    f'sym_h_pair_{idx}_rgl'
                )

                b_cumul = self._model.NewBoolVar(f'sym_h_cumul_{idx}')
                if prev_cumul is None:
                    self._model.AddImplication(b_cumul, b_lgr)
                    self._model.AddImplication(b_cumul, b_rgl)
                    self._model.AddBoolOr([b_cumul, b_lgr.Not(), b_rgl.Not()])
                else:
                    self._model.AddImplication(b_cumul, prev_cumul)
                    self._model.AddImplication(b_cumul, b_lgr)
                    self._model.AddImplication(b_cumul, b_rgl)
                    self._model.AddBoolOr([b_cumul, prev_cumul.Not(), b_lgr.Not(), b_rgl.Not()])

                b_eq_extend = self._model.NewBoolVar(f'sym_h_ext_{idx}')
                var_left = self._island_bridges_z3[position_left][Direction.left()]
                var_right = self._island_bridges_z3[position_right][Direction.right()]
                self._model.Add(var_left == var_right).OnlyEnforceIf(b_eq_extend)
                self._model.Add(var_left != var_right).OnlyEnforceIf(b_eq_extend.Not())

                b_impl = self._model.NewBoolVar(f'sym_h_impl_{idx}')
                self._model.AddBoolOr([b_impl.Not(), b_cumul.Not(), b_eq_extend])
                self._model.AddBoolOr([b_cumul, b_impl])
                self._model.AddBoolOr([b_eq_extend.Not(), b_impl])

                all_sub_bools.append(b_impl)

                prev_cumul = b_cumul
                position_left = position_left.left
                position_right = position_right.right
                idx += 1
        else:
            position_left = Position(dot_position.r, int(dot_position.c))
            position_right = position_left.right
            pairs = [
                (self._island_bridges_z3[position_left][Direction.right()], 1),
                (self._island_bridges_z3[position_right][Direction.left()], 1),
            ]
            b = self._pairs_to_boolvar(pairs, f'sym_h_base_{dot_position}')
            all_sub_bools.append(b)

            prev_cumul = b
            idx = 0
            while position_left in self._input_grid and position_right in self._input_grid:
                b_lgr = self._pairs_to_boolvar(
                    [(self._island_bridges_z3[position_left][Direction.right()], 1)],
                    f'sym_h_pair_{idx}_lgr'
                )
                b_rgl = self._pairs_to_boolvar(
                    [(self._island_bridges_z3[position_right][Direction.left()], 1)],
                    f'sym_h_pair_{idx}_rgl'
                )

                b_cumul = self._model.NewBoolVar(f'sym_h_cumul_{idx}')
                self._model.AddImplication(b_cumul, prev_cumul)
                self._model.AddImplication(b_cumul, b_lgr)
                self._model.AddImplication(b_cumul, b_rgl)
                self._model.AddBoolOr([b_cumul, prev_cumul.Not(), b_lgr.Not(), b_rgl.Not()])

                b_eq_extend = self._model.NewBoolVar(f'sym_h_ext_{idx}')
                var_left = self._island_bridges_z3[position_left][Direction.left()]
                var_right = self._island_bridges_z3[position_right][Direction.right()]
                self._model.Add(var_left == var_right).OnlyEnforceIf(b_eq_extend)
                self._model.Add(var_left != var_right).OnlyEnforceIf(b_eq_extend.Not())

                b_impl = self._model.NewBoolVar(f'sym_h_impl_{idx}')
                self._model.AddBoolOr([b_impl.Not(), b_cumul.Not(), b_eq_extend])
                self._model.AddBoolOr([b_cumul, b_impl])
                self._model.AddBoolOr([b_eq_extend.Not(), b_impl])

                all_sub_bools.append(b_impl)

                prev_cumul = b_cumul
                position_left = position_left.left
                position_right = position_right.right
                idx += 1

        if not all_sub_bools:
            return None
        b_block = self._model.NewBoolVar(f'sym_h_block_{dot_position}')
        for b_sub in all_sub_bools:
            self._model.AddImplication(b_block, b_sub)
        return b_block

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(
                        self._island_bridges_z3[island.position][direction]
                        == self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite]
                    )
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)
