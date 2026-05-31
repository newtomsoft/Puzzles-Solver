from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.Heyawake.HeyawakeSolver import HeyawakeSolver


class AyeheyaSolver(HeyawakeSolver):
    def __init__(self, grid: Grid, region_grid: Grid):
        super().__init__(grid, region_grid)

    def _add_constraints(self):
        super()._add_constraints()
        self._add_rotational_symmetry_constraints()

    def _add_rotational_symmetry_constraints(self):
        for region in self.regions.values():
            region_positions = list(region)
            if len(region_positions) <= 1:
                continue

            center_r = sum(p.r for p in region_positions) / len(region_positions)
            center_c = sum(p.c for p in region_positions) / len(region_positions)

            seen = set()
            for position in region_positions:
                symmetric_r = 2 * center_r - position.r
                symmetric_c = 2 * center_c - position.c
                symmetric_position = Position(round(symmetric_r), round(symmetric_c))

                if symmetric_position == position:
                    continue

                if symmetric_position not in seen and symmetric_position in region:
                    seen.add(position)
                    seen.add(symmetric_position)
                    self._model.add(self._grid_vars[position] == self._grid_vars[symmetric_position])
