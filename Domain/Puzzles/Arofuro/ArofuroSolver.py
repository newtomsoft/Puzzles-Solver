from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class ArofuroSolver(GameSolver):
    Empty = None
    Black = 'B'
    up = 1
    down = 2
    right = 3
    left = 4

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars = None
        self._region_id_vars = None
        self._rank_vars = None
        self._previous_solution = Grid.empty()
        self._solver = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.NewIntVar(0, 4, f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._region_id_vars = Grid([[self._model.NewIntVar(-1, self._rows_number * self._columns_number, f"region_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._rank_vars = Grid([[self._model.NewIntVar(0, self._rows_number * self._columns_number, f"rank_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def solution_to_string(self) -> str:
        value_by_arrow = {0: '•', 1: '↑', 2: '↓', 3: '→', 4: '←'}
        if self._solver is None:
            self.get_solution()

        grid_str = ""
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                grid_str += value_by_arrow[self._previous_solution[r][c]] + " "
            grid_str += "\n"

        return grid_str.strip('\n')

    def get_solution(self) -> Grid:
        if self._solver is None:
            self._init_solver()

        self._solver = cp_model.CpSolver()
        status = self._solver.Solve(self._model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution_grid = Grid([[self._solver.Value(self._grid_vars[r][c]) for c in range(self._columns_number)] for r in range(self._rows_number)])
            self._previous_solution = solution_grid
            return solution_grid
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution == Grid.empty():
            return self.get_solution()

        negated_constraints_bools = []
        for position, _ in self._grid:
            if self._previous_solution[position] != 0:  # Only constrain arrows
                b = self._model.NewBoolVar(f"neq_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] != self._previous_solution[position]).OnlyEnforceIf(b)
                self._model.Add(self._grid_vars[position] == self._previous_solution[position]).OnlyEnforceIf(b.Not())
                negated_constraints_bools.append(b)
        
        if not negated_constraints_bools:
            return Grid.empty()

        self._model.AddBoolOr(negated_constraints_bools)
        return self.get_solution()

    def _add_constraints(self):
        self._add_domain_constraints()
        self._add_input_constraints()
        self._add_adjacency_constraints()
        self._add_flow_constraints()
        self._add_count_constraints()

    def _add_domain_constraints(self):
        # Already handled by variable initialization
        pass

    def _add_input_constraints(self):
        for position, val in self._grid:
            if val == self.Black:
                self._model.Add(self._grid_vars[position] == 0)
                self._model.Add(self._rank_vars[position] == 0)
                self._model.Add(self._region_id_vars[position] == -1)
            elif val != self.Empty:
                self._model.Add(self._grid_vars[position] == 0)
                self._model.Add(self._rank_vars[position] == 0)
                region_id = self._grid.get_index_from_position(position) + 1
                self._model.Add(self._region_id_vars[position] == region_id)
            else: # Arrow cell
                self._model.Add(self._grid_vars[position] >= 1)
                self._model.Add(self._rank_vars[position] > 0)

    def _add_adjacency_constraints(self):
        for position, _ in self._grid:
            current = self._grid_vars[position]

            # Right neighbor
            right_pos = position.right
            if right_pos in self._grid:
                right = self._grid_vars[right_pos]

                b_current = self._model.NewBoolVar("")
                self._model.Add(current > 0).OnlyEnforceIf(b_current)
                self._model.Add(current == 0).OnlyEnforceIf(b_current.Not())

                b_right = self._model.NewBoolVar("")
                self._model.Add(right > 0).OnlyEnforceIf(b_right)
                self._model.Add(right == 0).OnlyEnforceIf(b_right.Not())

                self._model.Add(current != right).OnlyEnforceIf([b_current, b_right])

            # Bottom neighbor
            bottom_pos = position.down
            if bottom_pos in self._grid:
                bottom = self._grid_vars[bottom_pos]

                b_current = self._model.NewBoolVar("")
                self._model.Add(current > 0).OnlyEnforceIf(b_current)
                self._model.Add(current == 0).OnlyEnforceIf(b_current.Not())

                b_bottom = self._model.NewBoolVar("")
                self._model.Add(bottom > 0).OnlyEnforceIf(b_bottom)
                self._model.Add(bottom == 0).OnlyEnforceIf(b_bottom.Not())

                self._model.Add(current != bottom).OnlyEnforceIf([b_current, b_bottom])

    def _add_flow_constraints(self):
        for position, _ in self._grid:
            # North
            north_pos = position.up
            if north_pos in self._grid:
                points_north = self._model.NewBoolVar(f"points_north_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] == self.up).OnlyEnforceIf(points_north)
                self._model.Add(self._grid_vars[position] != self.up).OnlyEnforceIf(points_north.Not())

                self._model.Add(self._region_id_vars[position] == self._region_id_vars[north_pos]).OnlyEnforceIf(points_north)
                self._model.Add(self._rank_vars[position] == self._rank_vars[north_pos] + 1).OnlyEnforceIf(points_north)
            else:
                self._model.Add(self._grid_vars[position] != self.up)

            # South
            south_pos = position.down
            if south_pos in self._grid:
                points_south = self._model.NewBoolVar(f"points_south_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] == self.down).OnlyEnforceIf(points_south)
                self._model.Add(self._grid_vars[position] != self.down).OnlyEnforceIf(points_south.Not())

                self._model.Add(self._region_id_vars[position] == self._region_id_vars[south_pos]).OnlyEnforceIf(points_south)
                self._model.Add(self._rank_vars[position] == self._rank_vars[south_pos] + 1).OnlyEnforceIf(points_south)
            else:
                self._model.Add(self._grid_vars[position] != self.down)

            # East
            east_pos = position.right
            if east_pos in self._grid:
                points_east = self._model.NewBoolVar(f"points_east_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] == self.right).OnlyEnforceIf(points_east)
                self._model.Add(self._grid_vars[position] != self.right).OnlyEnforceIf(points_east.Not())

                self._model.Add(self._region_id_vars[position] == self._region_id_vars[east_pos]).OnlyEnforceIf(points_east)
                self._model.Add(self._rank_vars[position] == self._rank_vars[east_pos] + 1).OnlyEnforceIf(points_east)
            else:
                self._model.Add(self._grid_vars[position] != self.right)

            # West
            west_pos = position.left
            if west_pos in self._grid:
                points_west = self._model.NewBoolVar(f"points_west_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] == self.left).OnlyEnforceIf(points_west)
                self._model.Add(self._grid_vars[position] != self.left).OnlyEnforceIf(points_west.Not())

                self._model.Add(self._region_id_vars[position] == self._region_id_vars[west_pos]).OnlyEnforceIf(points_west)
                self._model.Add(self._rank_vars[position] == self._rank_vars[west_pos] + 1).OnlyEnforceIf(points_west)
            else:
                self._model.Add(self._grid_vars[position] != self.left)

    def _add_count_constraints(self):
        for position, val in self._grid:
            if val is not None and val != self.Black:
                region_id = self._grid.get_index_from_position(position) + 1

                region_indicators = []
                for r in range(self._rows_number):
                    for c in range(self._columns_number):
                        indicator = self._model.NewBoolVar(f"in_region_{region_id}_{r}_{c}")
                        self._model.Add(self._region_id_vars[r][c] == region_id).OnlyEnforceIf(indicator)
                        self._model.Add(self._region_id_vars[r][c] != region_id).OnlyEnforceIf(indicator.Not())
                        region_indicators.append(indicator)

                self._model.Add(sum(region_indicators) == val + 1)
