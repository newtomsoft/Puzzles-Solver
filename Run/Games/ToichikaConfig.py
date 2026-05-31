from PuzzleSolver.Puzzles.Toichika.ToichikaSolver import ToichikaSolver
from GridPlayers.GridPuzzle.GridPuzzleToichikaPlayer import GridPuzzleToichikaPlayer
from GridProviders.GridPuzzle.GridPuzzleToichikaGridProvider import GridPuzzleToichikaGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/toichika",
        GridPuzzleToichikaGridProvider,
        GridPuzzleToichikaPlayer
    )(ToichikaSolver)
