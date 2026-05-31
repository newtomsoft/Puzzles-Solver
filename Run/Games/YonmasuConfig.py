from PuzzleSolver.Puzzles.Yonmasu.YonmasuSolver import YonmasuSolver
from GridPlayers.GridPuzzle.GridPuzzleYonmasuPlayer import GridPuzzleYonmasuPlayer
from GridProviders.GridPuzzle.GridPuzzleYonmasuGridProvider import GridPuzzleYonmasuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/yonmasu",
        GridPuzzleYonmasuGridProvider,
        GridPuzzleYonmasuPlayer
    )(YonmasuSolver)
