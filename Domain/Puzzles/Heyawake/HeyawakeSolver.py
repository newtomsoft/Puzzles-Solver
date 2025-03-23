from Domain.Grid.Grid import Grid
from Domain.Position import Position
from GameSolver import GameSolver
from Ports.SolverEngine import SolverEngine
from Utils.ShapeGenerator import ShapeGenerator


class HeyawakeSolver(GameSolver):
    def __init__(self, grid: Grid, region_grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.regions = region_grid.get_regions()
        if len(self.regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[self._solver.bool(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.has_constraints():
            self._init_solver()

        solution, _ = self._ensure_all_white_connected()
        self._previous_solution = solution
        return solution

    def _ensure_all_white_connected(self):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[self._solver.is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self._grid.columns_number)] for i in range(self._grid.rows_number)])
            white_shapes = current_grid.get_all_shapes()
            if len(white_shapes) == 1:
                return current_grid, proposition_count

            biggest_white_shapes = max(white_shapes, key=len)
            white_shapes.remove(biggest_white_shapes)
            for white_shape in white_shapes:
                around_white = ShapeGenerator.around_shape(white_shape)
                around_white_are_not_all_black_constraint = self._solver.Not(self._solver.And([self._solver.Not(self._grid_z3[position]) for position in around_white if position in self._grid]))
                self._solver.add(around_white_are_not_all_black_constraint)

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for position, _ in [(position, value) for (position, value) in self._previous_solution if not value]:
            previous_solution_constraints.append(self._solver.Not(self._grid_z3[position]))
        self._solver.add(self._solver.Not(self._solver.And(previous_solution_constraints)))

        return self.get_solution()

    def _add_constraints(self):
        self._add_black_cell_count_in_regions_constraints()
        self._add_no_adjacent_black_cells_touching_constraints()
        self._add_white_segment_not_crossing_more_2_regions_constraints()

    def _add_black_cell_count_in_regions_constraints(self):
        for region in self.regions.values():
            black_cells_count_position = min([position for position in region], key=lambda p: (p.r, p.c))
            black_cells_count = self._grid[black_cells_count_position]
            if not isinstance(black_cells_count, int) or black_cells_count < 0:
                continue
            self._solver.add(self._solver.sum([self._solver.Not(self._grid_z3[position]) for position in region]) == black_cells_count)

    def _add_no_adjacent_black_cells_touching_constraints(self):
        for position, value in self._grid_z3:
            for neighbor_position in self._grid.neighbors_positions(position):
                self._solver.add(self._solver.Implies(self._solver.Not(self._grid_z3[position]), self._grid_z3[neighbor_position]))

    def _add_white_segment_not_crossing_more_2_regions_constraints(self):
        for row in range(self._grid.rows_number):
            positions = [Position(row, column) for column in range(self._grid.columns_number)]
            self._add_white_segment_not_crossing_more_2_regions_constraints_in_positions(positions)
        for column in range(self._grid.columns_number):
            positions = [Position(row, column) for row in range(self._grid.rows_number)]
            self._add_white_segment_not_crossing_more_2_regions_constraints_in_positions(positions)

    def _add_white_segment_not_crossing_more_2_regions_constraints_in_positions(self, positions: list[Position]):
        regions = {}
        for position in positions:
            region_id = 0
            for current_region_id, region_positions in self.regions.items():
                if position in region_positions:
                    region_id = current_region_id
                    continue
            regions.setdefault(region_id, []).append(position)
        if len(regions) <= 2:
            return
        keys_regions = list(regions.keys())
        for index_region, key_region in enumerate(keys_regions[1:-1]):
            previous_key_region = keys_regions[index_region]
            next_key_region = keys_regions[index_region + 2]
            constraint_all_white = self._solver.And([self._grid_z3[position] for position in regions[key_region]])
            constraint_at_least_1_neighbor_black = self._solver.Or([self._solver.Not(self._grid_z3[position]) for position in [regions[previous_key_region][-1]] + [regions[next_key_region][0]]])
            self._solver.add(self._solver.Implies(constraint_all_white, constraint_at_least_1_neighbor_black))
