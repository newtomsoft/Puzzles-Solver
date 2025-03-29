from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from GameSolver import GameSolver


class VectorsSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None
        self._black_positions_with_region_number: dict[Position, int] = {}

    def get_solution(self) -> (Grid, int):
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if not self._solver.has_solution():
            return Grid.empty()
        return Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_regions_constraints()
        self._add_regions_size_constraints()
        self._add_regions_in_1_block_constraints()

    def _add_initial_constraints(self):
        black_cell_count = [1 for position, value in self._grid if type(value) is int and value >= 0].count(1)
        region_number = 0
        for position, value in self._grid:
            if type(value) is int and value >= 0:
                region_number += 1
                self._black_positions_with_region_number[position] = region_number
                self._solver.add(self._grid_z3[position] == region_number)
            else:
                self._solver.add(1 <= self._grid_z3[position])
                self._solver.add(self._grid_z3[position] <= black_cell_count)

    def _add_regions_constraints(self):
        positions_possible_region_values: dict[Position, list] = {}
        for current_position, region_number in self._black_positions_with_region_number.items():
            for position in [pos for pos in self._grid.all_orthogonal_positions(current_position) if pos not in self._black_positions_with_region_number and current_position.distance_to(pos) <= self._grid[current_position]]:
                if position not in positions_possible_region_values:
                    positions_possible_region_values[position] = []
                positions_possible_region_values[position].append(self._grid_z3[position] == region_number)
        for position, possible_region_values in positions_possible_region_values.items():
            self._solver.add(self._solver.Or(possible_region_values))

    def _add_regions_size_constraints(self):
        for position, region_number in self._black_positions_with_region_number.items():
            count_for_this_region = self._grid[position] + 1
            self._solver.add(sum([self._solver.sum(value == region_number) for _, value in self._grid_z3]) == count_for_this_region)

    def _add_regions_in_1_block_constraints(self):
        for position, region_number in self._black_positions_with_region_number.items():
            for up_position in self._grid.all_positions_up(position)[-1:0:-1]:
                self._solver.add(self._solver.Implies(self._grid_z3[up_position] == region_number, self._grid_z3[up_position.down] == region_number))
            for down_position in self._grid.all_positions_down(position)[-1:0:-1]:
                self._solver.add(self._solver.Implies(self._grid_z3[down_position] == region_number, self._grid_z3[down_position.up] == region_number))
            for left_position in self._grid.all_positions_left(position)[-1:0:-1]:
                self._solver.add(self._solver.Implies(self._grid_z3[left_position] == region_number, self._grid_z3[left_position.right] == region_number))
            for right_position in self._grid.all_positions_right(position)[-1:0:-1]:
                self._solver.add(self._solver.Implies(self._grid_z3[right_position] == region_number, self._grid_z3[right_position.left] == region_number))
