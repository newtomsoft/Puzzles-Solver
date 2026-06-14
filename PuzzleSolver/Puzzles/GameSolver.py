import random
from abc import ABC, abstractmethod

from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid


_SEED_MAX = 2**31 - 1 # max int32 pour or-tools


class GameSolver(ABC):
    cell_empty = None
    cell_outside = '#'
    cell_blocked = '🛇'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._solver = cp_model.CpSolver()
        self._randomize_solver_seed(self._solver)

    @staticmethod
    def _randomize_solver_seed(solver: cp_model.CpSolver) -> None:
        solver.parameters.random_seed = random.randint(0, _SEED_MAX)

    @abstractmethod
    def get_solution(self) -> Grid:
        pass

    @abstractmethod
    def get_other_solution(self) -> Grid:
        pass

    def get_stats(self) -> dict:
        """Return solver statistics. Must be called after get_solution()."""
        return {
            "num_conflicts": self._solver.num_conflicts,
            "num_branches": self._solver.num_branches,
            "wall_time": self._solver.wall_time,
        }

    def configure_for_difficulty_analysis(self) -> None:
        """Configure the underlying CP-SAT solver to produce meaningful search statistics
        (num_branches, num_conflicts) for difficulty estimation.

        - Limits presolve so the solver actually explores the search tree instead of
          solving everything at the root via propagation.
        - Forces single-threaded search + fixed seed for stable, reproducible difficulty
          scores across runs for the same puzzle.

        This is the recommended way for DifficultyAnalyzer classes. It follows the
        established pattern used by SudokuDifficultyAnalyzer and PutteriaDifficultyAnalyzer.
        """
        self._solver.parameters.max_presolve_iterations = 0
        self._solver.parameters.num_search_workers = 1
        self._solver.parameters.random_seed = 0