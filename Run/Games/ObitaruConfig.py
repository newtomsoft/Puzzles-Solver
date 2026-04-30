from Domain.Puzzles.Obitaru.ObitaruSolver import ObitaruSolver
from GridPlayers.GridPuzzle.GridPuzzleObitaruPlayer import GridPuzzleObitaruPlayer
from GridProviders.GridPuzzle.GridPuzzleObitaruGridProvider import GridPuzzleObitaruGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/obitaru",
        GridPuzzleObitaruGridProvider,
        GridPuzzleObitaruPlayer
    )(ObitaruSolver)
