from collections import defaultdict

from Board.Position import Position
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

    def _compute_regions_length(self):
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
        if not self._solver.has_solution():
            return Grid.empty()

        solution = Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        self._previous_solution = solution
        return solution

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_regions_lengths_constraints()
        self._add_distinct_in_regions_constraints()
        self._add_connected_cells_regions_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(value >= 1)
            self._solver.add(value <= self._regions_count)

    def _add_regions_lengths_constraints(self):
        for region_id, region_size in self._region_id_length.items():
            constraint = self._solver.sum([self._solver.If(value == region_id, 1, 0) for _, value in self._grid_z3]) == region_size
            self._solver.add(constraint)

    def _add_distinct_in_regions_constraints(self):
        for region_id, _ in self._region_id_length.items():
            constraint = self._solver.distinct([self._solver.If(value == region_id, self._grid[position], self._get_unique_value_for(position)) for position, value in self._grid_z3])
            self._solver.add(constraint)

    def _add_connected_cells_regions_constraints(self):
        steps = [Grid([[self._solver.int(f'step{region_id}_{r}_{c}') for c in range(self.columns_number)] for r in range(self.rows_number)]) for region_id in range(1, self._regions_count + 1)]
        for region_id, region_size in self._region_id_length.items():
            self._add_connected_cells_region_constraints(steps[region_id - 1], region_id)

    def _add_connected_cells_region_constraints(self, step: Grid, region_id: int):
        self._solver.add([self._solver.If(self._grid_z3[position] == region_id, step[position] >= 1, step[position] == 0) for position, _ in self._grid])
        roots = []
        for position, _ in self._grid_z3:
            roots.append(self._solver.And(self._grid_z3[position] == region_id, step[position] == 1))
        self._solver.add(self._solver.Or(roots))
        for i in range(len(roots)):
            for j in range(i + 1, len(roots)):
                self._solver.add(self._solver.Not(self._solver.And(roots[i], roots[j])))
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                current_step = step[i][j]
                adjacents = []
                if i > 0:
                    adjacents.append(self._solver.And(self._grid_z3[i - 1][j] == region_id, step[i - 1][j] == current_step - 1))
                if i < self.rows_number - 1:
                    adjacents.append(self._solver.And(self._grid_z3[i + 1][j] == region_id, step[i + 1][j] == current_step - 1))
                if j > 0:
                    adjacents.append(self._solver.And(self._grid_z3[i][j - 1] == region_id, step[i][j - 1] == current_step - 1))
                if j < self.columns_number - 1:
                    adjacents.append(self._solver.And(self._grid_z3[i][j + 1] == region_id, step[i][j + 1] == current_step - 1))

                self._solver.add(self._solver.Implies(self._solver.And(self._grid_z3[i][j] == region_id, current_step > 1), self._solver.Or(adjacents)))

    def _get_unique_value_for(self, position: Position) -> int:
        max_cell_value = max(self._numbers_occurs_in_regions.keys())
        hash_position = hash(position)
        return hash_position if hash_position <= 0 else hash_position + max_cell_value
