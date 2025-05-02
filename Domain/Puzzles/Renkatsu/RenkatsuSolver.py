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
        self._regions_count = self._numbers_count[1]
        self._compute_regions_length()

    def _compute_numbers_occurs_in_regions(self):
        self._numbers_count = defaultdict(int)
        for _, value in self._grid:
            self._numbers_count[value] += 1

    def _compute_regions_length(self):
        self._region_size_by_id = defaultdict(int)
        region_count = 0
        current_region_id = 1
        for number, number_count in sorted(self._numbers_count.items(), reverse=True):
            remaining_region_count = number_count - region_count
            if remaining_region_count == 0:
                continue
            region_count += remaining_region_count
            for i in range(current_region_id, current_region_id + remaining_region_count):
                self._region_size_by_id[i] = number
            current_region_id += remaining_region_count

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        constraints = []
        for region_id in range(1, self._regions_count + 1):
            current_region_positions = [position for position, value in self._previous_solution if value == region_id]
            same_value_in_this_region = []
            for i in range(1, len(current_region_positions)):
                same_value_in_this_region.append(self._grid_z3[current_region_positions[0]] == self._grid_z3[current_region_positions[i]])
            constraints.append(self._solver.And(same_value_in_this_region))
        self._solver.add(self._solver.Not(self._solver.And(constraints)))

        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        if not self._solver.has_solution():
            return Grid.empty()

        non_ordered_solution = Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        solution = self._order_values_by_position(non_ordered_solution)
        self._previous_solution = solution
        return solution

    def _add_constraints(self):
        self._add_same_numbers_in_distincts_regions_constraints()
        self._add_regions_size_constraints()
        self._add_connected_cells_regions_constraints()

    def _add_same_numbers_in_distincts_regions_constraints(self):
        for number in self._numbers_count.keys():
            self._solver.add(self._solver.distinct([self._grid_z3[position] for position, value in self._grid if value == number]))

    def _add_regions_size_constraints(self):
        for region_id, region_size in self._region_size_by_id.items():
            self._solver.add(self._solver.sum([cell_value == region_id for _, cell_value in self._grid_z3]) == region_size)

    def _add_connected_cells_regions_constraints(self):
        steps = [Grid([[self._solver.int(f'step{region_id}_{r}_{c}') for c in range(self.columns_number)] for r in range(self.rows_number)]) for region_id in range(1, self._regions_count + 1)]
        for region_id, region_size in self._region_size_by_id.items():
            self._add_connected_cells_region_constraints(steps[region_id - 1], region_id)

    def _add_connected_cells_region_constraints(self, step: Grid, region_id: int):
        self._solver.add([self._solver.If(self._grid_z3[position] == region_id, step[position] >= 1, step[position] == 0) for position, _ in self._grid])

        roots = [self._solver.And(self._grid_z3[position] == region_id, step[position] == 1) for position, _ in self._grid]
        self._solver.add(self._solver.Or(roots))

        self._solver.add([self._solver.Not(self._solver.And(roots[i], roots[j])) for i in range(len(roots)) for j in range(i + 1, len(roots))])

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                current_step = step[r][c]
                adjacents = []
                if r > 0:
                    adjacents.append(self._solver.And(self._grid_z3[r - 1][c] == region_id, step[r - 1][c] == current_step - 1))
                if r < self.rows_number - 1:
                    adjacents.append(self._solver.And(self._grid_z3[r + 1][c] == region_id, step[r + 1][c] == current_step - 1))
                if c > 0:
                    adjacents.append(self._solver.And(self._grid_z3[r][c - 1] == region_id, step[r][c - 1] == current_step - 1))
                if c < self.columns_number - 1:
                    adjacents.append(self._solver.And(self._grid_z3[r][c + 1] == region_id, step[r][c + 1] == current_step - 1))

                self._solver.add(self._solver.Implies(self._solver.And(self._grid_z3[r][c] == region_id, current_step > 1), self._solver.Or(adjacents)))

    def _order_values_by_position(self, old_grid: Grid) -> Grid:
        new_value_by_old_value = {}
        current_value = 1
        new_grid = Grid([[0 for _ in range(self.columns_number)] for _ in range(self.rows_number)])
        for position, old_value in old_grid:
            if not (new_value := new_value_by_old_value.get(old_value)):
                new_value_by_old_value[old_value] = current_value
                new_value = current_value
                current_value += 1
            new_grid.set_value(position, new_value)

        return new_grid
