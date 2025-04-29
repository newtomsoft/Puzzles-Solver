from collections import defaultdict

from Domain.Board.Grid import Grid
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver


class RenkatsuSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None
        self._compute_numbers_occurs_in_regions()
        self._regions_count = self._numbers_occurs_in_regions[1]
        self._compute_regions_length()

    def _compute_numbers_occurs_in_regions(self):
        self._numbers_occurs_in_regions = defaultdict(int)
        for _, value in self._grid:
            self._numbers_occurs_in_regions[value] += 1

    def _compute_regions_length(self): # KO
        self._region_id_length = defaultdict(int)
        region_count = 0
        region_id = 1
        for number_region in sorted(self._numbers_occurs_in_regions.items(), reverse=True):
            remaining_region_count = number_region[1] - region_count
            if remaining_region_count == 0:
                continue
            region_count += remaining_region_count
            for i in range(region_id, region_id + remaining_region_count):
                self._region_id_length[i] = number_region[0]
            region_id += remaining_region_count

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in self._previous_solution if value > 0])))
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        while self._solver.has_solution():
            matrix_number = [[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)]
            attempt = Grid(matrix_number)
            connected = True
            for region_id in range(1, self._regions_count + 1):
                connected = attempt.are_cells_connected(region_id)
                if not connected:
                    self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in attempt])))
                    break
            if not connected:
                continue
            self._previous_solution = attempt
            return attempt
        return Grid.empty()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_count_constraints()
        self._add_distinct_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(value >= 1)
            self._solver.add(value <= self._regions_count)

    def _add_count_constraints(self):
        for region_id, length in self._region_id_length.items():
            constraint = self._solver.sum([self._solver.If(value == region_id, 1, 0) for _, value in self._grid_z3]) == length
            self._solver.add(constraint)

    def _add_distinct_constraints(self):
        for region_id, length in self._region_id_length.items():
            constraint = self._solver.distinct([self._solver.If(value == region_id, self._grid[position], hash(position) * 100) for position, value in self._grid_z3])
            self._solver.add(constraint)
