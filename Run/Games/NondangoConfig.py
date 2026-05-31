from PuzzleSolver.Puzzles.Nondango.NondangoSolver import NondangoSolver
from GridPlayers.GridPuzzle.GridPuzzleNondangoPlayer import GridPuzzleNondangoPlayer
from GridProviders.GridPuzzle.GridPuzzleNondangoGridProvider import GridPuzzleNondangoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/nondango",
        GridPuzzleNondangoGridProvider,
        GridPuzzleNondangoPlayer
    )(NondangoSolver)
