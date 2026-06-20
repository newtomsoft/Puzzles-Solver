from .shapes import ALL_SHAPES, REGION_SIZE
from PuzzleSolver.Puzzles.Foseruzu.SameSizeRegionsSolver import SameSizeRegionsSolver


class FourSixOneTwoSolver(SameSizeRegionsSolver):
    REGION_SIZE = REGION_SIZE
    ALL_SHAPES = ALL_SHAPES

    def _init_solver(self):
        nb_clues = sum(1 for _, v in self._grid if v not in (self.cell_empty, self.cell_outside))
        total = self._active_count
        if nb_clues * 4 == total or nb_clues * 3 == total:
            raise ValueError(
                f"Degenerate puzzle: {nb_clues} clues with {total} active cells "
                f"forces all regions to be the same size "
                f"(all-4: {nb_clues}×4={nb_clues*4}, "
                f"all-6: {nb_clues}×3={nb_clues*3})."
            )
        super()._init_solver()

    def _add_specific_constraints(self):
        for p, cells in enumerate(self._placements):
            clue_count = sum(1 for i, j in cells if self._grid[(i, j)] not in (self.cell_empty, self.cell_outside))
            if len(cells) == 4:
                self._model.add(clue_count == 1).only_enforce_if(self._use[p])
            elif len(cells) == 6:
                self._model.add(clue_count == 2).only_enforce_if(self._use[p])
