from PuzzleSolver.Puzzles.Araf.ArafSolver import ArafSolver
from GridPlayers.GridPuzzle.GridPuzzleArafPlayer import GridPuzzleArafPlayer
from GridProviders.GridPuzzle.GridPuzzleArafGridProvider import GridPuzzleArafGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/araf",
        GridPuzzleArafGridProvider,
        GridPuzzleArafPlayer
    )(ArafSolver)
