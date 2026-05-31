from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class ToichikaSolver(GameSolver):
    Empty = 0
    Up = 1
    Down = 2
    Right = 3
    Left = 4

    def __init__(self, regions_grid: RegionsGrid, given_arrows: Grid):
        self._regions_grid = regions_grid
        self._given_arrows = given_arrows
        self._rows_number = regions_grid.rows_number
        self._columns_number = regions_grid.columns_number
        self._model = cp_model.CpModel()
        self._arrow_vars = None
        self._has_arrow_vars = {}
        self._paired_vars = {}
        self._valid_pairs = []
        self._previous_solution = Grid.empty()
        self._solver = None

    def get_solution(self) -> Grid:
        self._init_solver()
        self._solver = cp_model.CpSolver()
        status = self._solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            solution = Grid([[self._solver.value(self._arrow_vars[r][c]) for c in range(self._columns_number)] for r in range(self._rows_number)])
            self._previous_solution = solution
            return solution
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution == Grid.empty():
            return self.get_solution()
        literals = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                prev_val = self._previous_solution.value(r, c)
                if prev_val == 0:
                    continue
                b = self._model.new_bool_var(f"diff_{r}_{c}")
                self._model.add(self._arrow_vars[r][c] != prev_val).only_enforce_if(b)
                self._model.add(self._arrow_vars[r][c] == prev_val).only_enforce_if(b.negated())
                literals.append(b)
        if not literals:
            return Grid.empty()
        self._model.add_bool_or(literals)
        return self.get_solution()

    def _init_solver(self):
        self._arrow_vars = [[self._model.new_int_var(0, 4, f"arrow_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        self._has_arrow_vars = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                has_arrow = self._model.new_bool_var(f"has_arrow_{r}_{c}")
                self._model.add(self._arrow_vars[r][c] != 0).only_enforce_if(has_arrow)
                self._model.add(self._arrow_vars[r][c] == 0).only_enforce_if(has_arrow.negated())
                self._has_arrow_vars[pos] = has_arrow

        self._build_regions()
        self._build_valid_pairs()
        self._add_constraints()

    def _build_regions(self):
        self._region_cells = {}
        for position, region_id in self._regions_grid:
            if region_id not in self._region_cells:
                self._region_cells[region_id] = []
            self._region_cells[region_id].append(position)

    def _build_valid_pairs(self):
        self._valid_pairs = []
        self._paired_vars = {}

        # Precompute region adjacency (orthogonal)
        adjacent_regions = set()
        for position, region_id in self._regions_grid:
            for neighbor_pos in position.neighbors():
                if neighbor_pos in self._regions_grid:
                    neighbor_region = self._regions_grid[neighbor_pos]
                    if neighbor_region != region_id:
                        pair = tuple(sorted([region_id, neighbor_region]))
                        adjacent_regions.add(pair)

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                region_id = self._regions_grid[pos]
                # Same row to the right
                for cc in range(c + 1, self._columns_number):
                    other_pos = Position(r, cc)
                    other_region = self._regions_grid[other_pos]
                    if other_region == region_id:
                        continue
                    if tuple(sorted([region_id, other_region])) in adjacent_regions:
                        continue
                    pair = (pos, other_pos)
                    self._valid_pairs.append(pair)
                    self._paired_vars[pair] = self._model.new_bool_var(f"paired_{r}_{c}_{r}_{cc}")
                # Same column down
                for rr in range(r + 1, self._rows_number):
                    other_pos = Position(rr, c)
                    other_region = self._regions_grid[other_pos]
                    if other_region == region_id:
                        continue
                    if tuple(sorted([region_id, other_region])) in adjacent_regions:
                        continue
                    pair = (pos, other_pos)
                    self._valid_pairs.append(pair)
                    self._paired_vars[pair] = self._model.new_bool_var(f"paired_{r}_{c}_{rr}_{c}")

    def _add_constraints(self):
        self._add_region_constraints()
        self._add_given_arrow_constraints()
        self._add_pairing_constraints()
        self._add_pair_direction_constraints()
        self._add_between_constraints()

    def _add_region_constraints(self):
        for region_id, cells in self._region_cells.items():
            self._model.add(sum(self._has_arrow_vars[pos] for pos in cells) == 1)

    def _add_given_arrow_constraints(self):
        arrow_map = {self.Up: self.Up, self.Down: self.Down, self.Right: self.Right, self.Left: self.Left}
        for position, value in self._given_arrows:
            if value in arrow_map:
                self._model.add(self._arrow_vars[position.r][position.c] == arrow_map[value])

    def _add_pairing_constraints(self):
        for pos in [Position(r, c) for r in range(self._rows_number) for c in range(self._columns_number)]:
            incident_pairs = []
            for pair in self._valid_pairs:
                if pos in pair:
                    incident_pairs.append(self._paired_vars[pair])
            self._model.add(sum(incident_pairs) == self._has_arrow_vars[pos])

    def _add_pair_direction_constraints(self):
        direction_values = {
            Direction.up(): self.Up,
            Direction.down(): self.Down,
            Direction.right(): self.Right,
            Direction.left(): self.Left,
        }
        for (pos1, pos2), var in self._paired_vars.items():
            direction = pos1.direction_to(pos2)
            value1 = direction_values[direction]
            value2 = direction_values[direction.opposite]
            self._model.add(self._arrow_vars[pos1.r][pos1.c] == value1).only_enforce_if(var)
            self._model.add(self._arrow_vars[pos2.r][pos2.c] == value2).only_enforce_if(var)

    def _add_between_constraints(self):
        for (pos1, pos2), var in self._paired_vars.items():
            between_positions = pos1.all_positions_between(pos2)
            for between_pos in between_positions:
                self._model.add(self._arrow_vars[between_pos.r][between_pos.c] == 0).only_enforce_if(var)
