from PuzzleSolver.Puzzles.Mirukuti.MirukutiSolver import MirukutiSolver
from GridPlayers.GridPuzzle.GridPuzzleMirukutiPlayer import GridPuzzleMirukutiPlayer
from GridProviders.GridPuzzle.GridPuzzleMirukutiGridProvider import GridPuzzleMirukutiGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/mirukuti$",
        GridPuzzleMirukutiGridProvider,
        GridPuzzleMirukutiPlayer
    )(MirukutiSolver)
