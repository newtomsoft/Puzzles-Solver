from z3 import Solver, Int, And, Not, Implies, If, Sum, sat

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
        self._solver = Solver()
        self._grid_z3 = None
        self._region_id_z3 = None
        self._rank_z3 = None
        self._previous_solution = Grid.empty()

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._region_id_z3 = Grid([[Int(f"region_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._rank_z3 = Grid([[Int(f"rank_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def solution_to_string(self) -> str:
        value_by_arrow = {0: '•', 1: '↑', 2: '↓', 3: '→', 4: '←'}
        if not self._solver.assertions():
            self.get_solution()

        grid_str = ""
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                grid_str += value_by_arrow[self._previous_solution[r][c]] + " "
            grid_str += "\n"

        return grid_str.strip('\n')

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        if self._solver.check() == sat:
            model = self._solver.model()
            solution_grid = Grid([[model.eval(self._grid_z3[r][c]).as_long() for c in range(self._columns_number)] for r in range(self._rows_number)])
            self._previous_solution = solution_grid
            return solution_grid
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution == Grid.empty():
            return self.get_solution()

        constraints = []
        for position, _ in self._grid:
            if self._previous_solution[position] != 0:  # Only constrain arrows
                constraints.append(self._grid_z3[position] == self._previous_solution[position])

        self._solver.add(Not(And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_domain_constraints()
        self._add_input_constraints()
        self._add_adjacency_constraints()
        self._add_flow_constraints()
        self._add_count_constraints()

    def _add_domain_constraints(self):
        for position, _ in self._grid:
            self._solver.add(And(self._grid_z3[position] >= 0, self._grid_z3[position] <= 4))
            self._solver.add(self._rank_z3[position] >= 0)
            self._solver.add(self._region_id_z3[position] >= -1)

    def _add_input_constraints(self):
        number_cells = []
        for position, _ in self._grid:
            val = self._grid[position]
            if val == self.Black:
                self._solver.add(self._grid_z3[position] == 0)
                self._solver.add(self._rank_z3[position] == 0)
                # Assign a special region_id to BlackCells so arrows cannot point to them
                self._solver.add(self._region_id_z3[position] == -1)
            elif val != self.Empty:
                # It's a number cell
                self._solver.add(self._grid_z3[position] == 0)
                self._solver.add(self._rank_z3[position] == 0)
                # Unique region ID for each number cell. Let's use linear index + 1
                region_id = self._grid.get_index_from_position(position) + 1
                self._solver.add(self._region_id_z3[position] == region_id)
                number_cells.append(position)
            else:
                # It's an arrow cell
                self._solver.add(self._grid_z3[position] >= 1)
                self._solver.add(self._rank_z3[position] > 0)
                # Region ID must be one of the number cells' IDs
                # (Optimization: This is implicitly enforced by flow, but good to have bounds)

        # Optimization: If we know all possible region IDs, we could constrain them.
        # But flow constraints will handle it.

    def _add_adjacency_constraints(self):
        # No two orthogonally adjacent arrows can point in the same direction.
        for position, _ in self._grid:
            current = self._grid_z3[position]

            # Right neighbor
            right_pos = position.right
            if right_pos in self._grid:
                right = self._grid_z3[right_pos]
                self._solver.add(Implies(And(current > 0, right > 0), current != right))

            # Bottom neighbor
            bottom_pos = position.down
            if bottom_pos in self._grid:
                bottom = self._grid_z3[bottom_pos]
                self._solver.add(Implies(And(current > 0, bottom > 0), current != bottom))

    def _add_flow_constraints(self):
        for position, _ in self._grid:
            # If it's an arrow, it must point to a valid neighbor
            # And that neighbor must have the same region ID and lower rank

            # North
            north_pos = position.up
            if north_pos in self._grid:
                points_north = self._grid_z3[position] == self.up
                target_north = north_pos
                self._solver.add(Implies(points_north, And(
                    self._region_id_z3[position] == self._region_id_z3[target_north],
                    self._rank_z3[position] == self._rank_z3[target_north] + 1
                )))
            else:
                self._solver.add(self._grid_z3[position] != self.up)  # Cannot point North if at top edge

            # South
            south_pos = position.down
            if south_pos in self._grid:
                points_south = self._grid_z3[position] == self.down
                target_south = south_pos
                self._solver.add(Implies(points_south, And(
                    self._region_id_z3[position] == self._region_id_z3[target_south],
                    self._rank_z3[position] == self._rank_z3[target_south] + 1
                )))
            else:
                self._solver.add(self._grid_z3[position] != self.down)

            # East
            east_pos = position.right
            if east_pos in self._grid:
                points_east = self._grid_z3[position] == self.right
                target_east = east_pos
                self._solver.add(Implies(points_east, And(
                    self._region_id_z3[position] == self._region_id_z3[target_east],
                    self._rank_z3[position] == self._rank_z3[target_east] + 1
                )))
            else:
                self._solver.add(self._grid_z3[position] != self.right)

            # West
            west_pos = position.left
            if west_pos in self._grid:
                points_west = self._grid_z3[position] == self.left
                target_west = west_pos
                self._solver.add(Implies(points_west, And(
                    self._region_id_z3[position] == self._region_id_z3[target_west],
                    self._rank_z3[position] == self._rank_z3[target_west] + 1
                )))
            else:
                self._solver.add(self._grid_z3[position] != self.left)

    def _add_count_constraints(self):
        for position, _ in self._grid:
            val = self._grid[position]
            if val is not None and val != self.Black:
                region_id = self._grid.get_index_from_position(position) + 1

                count_in_region = Sum([If(self._region_id_z3[Position(i, j)] == region_id, 1, 0)
                                       for i in range(self._rows_number)
                                       for j in range(self._columns_number)])

                self._solver.add(count_in_region == val + 1)
