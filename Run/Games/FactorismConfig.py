from PuzzleSolver.Puzzles.Factorism.FactorismSolver import FactorismSolver
from GridPlayers.GridPuzzle.GridPuzzleFactorismPlayer import GridPuzzleFactorismPlayer
from GridProviders.GridPuzzle.GridPuzzleFactorismGridProvider import GridPuzzleFactorismGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/factorism",
        GridPuzzleFactorismGridProvider,
        GridPuzzleFactorismPlayer
    )(FactorismSolver)
