from collections import defaultdict

from z3 import Solver, Bool, Not, And, is_true, sat, BoolRef, Implies, Or

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class KakuteruAnpuSolver(GameSolver):
    def __init__(self, numbers_grid: Grid, regions_grid: Grid):
        self._numbers_grid = numbers_grid
        self._regions_grid = regions_grid
        self._regions = self._regions_grid.get_regions()
        self.rows_number = self._numbers_grid.rows_number
        self.columns_number = self._numbers_grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_black_cells_diagonally_connected()
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        previous_solution_constraints = []
        for position, _ in [(position, value) for (position, value) in self._previous_solution if not value]:
            previous_solution_constraints.append(Not(self._grid_z3[position]))
        self._solver.add(Not(And(previous_solution_constraints)))

        return self.get_solution()

    def _ensure_black_cells_diagonally_connected(self):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])

            black_shapes = current_grid.get_all_shapes(mode='diagonal')
            if len(black_shapes) == 1:
                return current_grid, proposition_count

            biggest_black_shapes = max(black_shapes, key=len)
            black_shapes.remove(biggest_black_shapes)
            for black_shape in black_shapes:
                in_all_black = And([Not(self._grid_z3[position]) for position in black_shape])
                around_all_withe = And([self._grid_z3[position] for position in ShapeGenerator.around_shape(black_shape) if position in self._grid_z3])
                constraint = Not(And(around_all_withe, in_all_black))
                self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def _add_constraints(self):
        self._add_black_regions_constraints()
        self._add_no_black_neighbors_between_regions_constraints()

    def _add_black_regions_constraints(self):
        for region in self._regions.values():
            self._add_black_region_constraint(region)

    def _add_black_region_constraint(self, region: frozenset[Position]):
        self._add_contiguity_constraint(region)
        number = max(0 if (number := self._numbers_grid[position]) is None else number for position in region)
        if number != 0:
            self._solver.add(sum([self._grid_z3[position] for position in region]) == number)

    def _add_contiguity_constraint(self, region: frozenset[Position]):
        region_sum = sum([self._grid_z3[position] for position in region])

        reach_vars: dict[tuple[int, int], BoolRef] = {}
        for pos in region:
            reach_vars[(pos.r, pos.c)] = Bool(f"reach_{pos.r}_{pos.c}")

        root_vars: dict[tuple[int, int], BoolRef] = {}
        for pos in region:
            root_vars[(pos.r, pos.c)] = Bool(f"root_{pos.r}_{pos.c}")

        no_black = (region_sum == 0)
        self._solver.add(Implies(no_black, sum([var for var in root_vars.values()]) == 0))

        self._solver.add(Implies(Not(no_black), sum([var for var in root_vars.values()]) == 1))

        for pos in region:
            pos_key = (pos.r, pos.c)
            self._solver.add(Implies(root_vars[pos_key], self._grid_z3[pos]))
            self._solver.add(Implies(root_vars[pos_key], reach_vars[pos_key]))

        neighbor_map = defaultdict(list)
        for pos in region:
            pos_key = (pos.r, pos.c)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor_key = (pos.r + dx, pos.c + dy)
                if neighbor_key in reach_vars:
                    neighbor_map[pos_key].append(neighbor_key)

        for pos in region:
            pos_key = (pos.r, pos.c)
            current_pos = self._grid_z3[pos]
            current_reach = reach_vars[pos_key]
            current_root = root_vars[pos_key]

            self._solver.add(Implies(current_pos, current_reach))
            self._solver.add(Implies(current_reach, current_pos))

            if neighbor_map[pos_key]:
                neighbor_reach_vars = [reach_vars[nk] for nk in neighbor_map[pos_key]]
                self._solver.add(Implies(And(current_reach, Not(current_root)), Or(neighbor_reach_vars)))

    def _add_no_black_neighbors_between_regions_constraints(self):
        for region in self._regions.values():
            self._add_no_black_neighbors_region_constraint(region)

    def _add_no_black_neighbors_region_constraint(self, region: frozenset[Position]):
        region_neighbors = ShapeGenerator.around_shape(region)
        for position in region:
            for position_neighbor in [neighbor for neighbor in self._numbers_grid.neighbors_positions(position) if neighbor in region_neighbors]:
                self._solver.add(Not(And(self._grid_z3[position], (self._grid_z3[position_neighbor]))))
