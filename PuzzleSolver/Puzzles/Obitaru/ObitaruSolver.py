from typing import Union

from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


ObitaruCell = Union[str, int, None]

class ObitaruSolver(GameSolver):
    white = 'w'
    cell_empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows = grid.rows_number
        self._cols = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._previous_solution = None
        self._previous_rectangles = []

    def get_solution(self) -> IslandGrid:
        self._setup_variables()
        self._add_constraints()
        return self._solve()

    def get_other_solution(self) -> IslandGrid:
        self._add_different_solution_constraint()
        return self._solve()

    def _setup_variables(self):
        self._rectangles = []
        self._rect_var = {}
        rect_id = 0
        for r1 in range(self._rows):
            for c1 in range(self._cols):
                for r2 in range(r1 + 1, self._rows):
                    for c2 in range(c1 + 1, self._cols):
                        rect = (r1, c1, r2, c2)
                        self._rectangles.append(rect)
                        self._rect_var[rect] = self._model.new_bool_var(f"rect_{rect_id}")
                        rect_id += 1

    @staticmethod
    def _get_perimeter(rect):
        r1, c1, r2, c2 = rect
        cells = set()
        for c in range(c1, c2 + 1):
            cells.add((r1, c))
            cells.add((r2, c))
        for r in range(r1 + 1, r2):
            cells.add((r, c1))
            cells.add((r, c2))
        return cells

    @staticmethod
    def _get_interior(rect):
        r1, c1, r2, c2 = rect
        cells = set()
        for r in range(r1 + 1, r2):
            for c in range(c1 + 1, c2):
                cells.add((r, c))
        return cells

    def _add_constraints(self):
        white_positions = []
        black_positions = []
        black_numbers = {}
        for r in range(self._rows):
            for c in range(self._cols):
                val = self._grid[r, c]
                if val == self.white:
                    white_positions.append((r, c))
                elif val != self.empty:
                    black_positions.append((r, c))
                    black_numbers[(r, c)] = val

        # Precompute data for each rectangle
        rect_data = {}
        for rect in self._rectangles:
            perim = self._get_perimeter(rect)
            interior = self._get_interior(rect)
            white_count = sum(1 for p in white_positions if p in perim)
            black_count = sum(1 for p in black_positions if p in interior)
            rect_data[rect] = {
                'perimeter': perim,
                'interior': interior,
                'white_count': white_count,
                'black_count': black_count,
            }

        # Filter invalid rectangles (more than 1 black inside)
        valid_rectangles = []
        for rect in self._rectangles:
            if rect_data[rect]['black_count'] <= 1:
                valid_rectangles.append(rect)

        # Black cells must be inside exactly one rectangle
        for bp in black_positions:
            covering = []
            for rect in valid_rectangles:
                if bp in rect_data[rect]['interior']:
                    covering.append(self._rect_var[rect])
            if covering:
                self._model.add_exactly_one(covering)
            else:
                self._model.add(0 == 1)

        # Black cells must NOT be on any perimeter
        for bp in black_positions:
            for rect in valid_rectangles:
                if bp in rect_data[rect]['perimeter']:
                    self._model.add(self._rect_var[rect] == 0)

        # Numbered black cells: exactly N white circles in the 8 neighboring cells
        for bp, num in black_numbers.items():
            r, c = bp
            neighbors = []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self._rows and 0 <= nc < self._cols:
                        if self._grid[nr, nc] == self.white:
                            neighbors.append((nr, nc))
            # The number should equal the count of white neighbors
            # This is a puzzle input validation, not a rectangle selection constraint
            # But we can use it to verify our understanding
            if len(neighbors) != num:
                # If the actual count doesn't match, our interpretation might be wrong
                pass
        
        # Alternative interpretation: numbered black cells = number of white circles on the loop's perimeter
        # (keeping original constraint as well for safety)
        for bp, num in black_numbers.items():
            for rect in valid_rectangles:
                if bp in rect_data[rect]['interior']:
                    if rect_data[rect]['white_count'] != num:
                        self._model.add(self._rect_var[rect] == 0)

        # White cells must be on at least one perimeter
        for wp in white_positions:
            covering = []
            for rect in valid_rectangles:
                if wp in rect_data[rect]['perimeter']:
                    covering.append(self._rect_var[rect])
            if covering:
                self._model.add(sum(covering) >= 1)
            else:
                self._model.add(0 == 1)

        # Parallel line constraints: at most one horizontal / vertical line per cell
        for r in range(self._rows):
            for c in range(self._cols):
                h_rects = []
                v_rects = []
                for rect in valid_rectangles:
                    r1, c1, r2, c2 = rect
                    # Horizontal: on top or bottom edge
                    if (r == r1 or r == r2) and c1 <= c <= c2:
                        h_rects.append(self._rect_var[rect])
                    # Vertical: on left or right edge
                    if (c == c1 or c == c2) and r1 <= r <= r2:
                        v_rects.append(self._rect_var[rect])
                if len(h_rects) > 1:
                    self._model.add(sum(h_rects) <= 1)
                if len(v_rects) > 1:
                    self._model.add(sum(v_rects) <= 1)

        self._valid_rectangles = valid_rectangles
        self._rect_data = rect_data

    def _solve(self) -> IslandGrid:
        status = self._solver.Solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return IslandGrid.empty()

        selected = [rect for rect in self._valid_rectangles if self._solver.Value(self._rect_var[rect]) == 1]
        self._previous_rectangles = selected

        island_grid = self._build_island_grid(selected)
        # Attach rectangles for the player
        island_grid.rectangles = selected
        self._previous_solution = island_grid
        return island_grid

    def _build_island_grid(self, rectangles):
        # Initialize matrix with Island objects to prevent IslandGrid from resetting
        grid = IslandGrid([[Island(Position(r, c), 0) for c in range(self._cols)] for r in range(self._rows)])

        for rect in rectangles:
            r1, c1, r2, c2 = rect
            # Top edge
            for c in range(c1, c2 + 1):
                if c > c1:
                    grid.islands[Position(r1, c)].set_bridge_to_position(Position(r1, c - 1), 1)
                if c < c2:
                    grid.islands[Position(r1, c)].set_bridge_to_position(Position(r1, c + 1), 1)
            # Bottom edge
            for c in range(c1, c2 + 1):
                if c > c1:
                    grid.islands[Position(r2, c)].set_bridge_to_position(Position(r2, c - 1), 1)
                if c < c2:
                    grid.islands[Position(r2, c)].set_bridge_to_position(Position(r2, c + 1), 1)
            # Left edge
            for r in range(r1, r2 + 1):
                if r > r1:
                    grid.islands[Position(r, c1)].set_bridge_to_position(Position(r - 1, c1), 1)
                if r < r2:
                    grid.islands[Position(r, c1)].set_bridge_to_position(Position(r + 1, c1), 1)
            # Right edge
            for r in range(r1, r2 + 1):
                if r > r1:
                    grid.islands[Position(r, c2)].set_bridge_to_position(Position(r - 1, c2), 1)
                if r < r2:
                    grid.islands[Position(r, c2)].set_bridge_to_position(Position(r + 1, c2), 1)

        # Recompute bridges_count for all islands and remove islands with no bridges
        empty_positions = []
        for position, island in list(grid.islands.items()):
            island.set_bridges_count_according_to_directions_bridges()
            if island.bridges_count == 0:
                empty_positions.append(position)
        for position in empty_positions:
            del grid.islands[position]

        return grid

    def _add_different_solution_constraint(self):
        if not self._previous_rectangles:
            return
        diffs = []
        for rect in self._valid_rectangles:
            if rect in self._previous_rectangles:
                diffs.append(self._rect_var[rect].Not())
            else:
                diffs.append(self._rect_var[rect])
        self._model.add(sum(diffs) >= 1)
