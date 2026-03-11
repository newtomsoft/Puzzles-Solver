from Domain.Puzzles.Mirukuti.MirukutiTeaseSolver import MirukutiTeaseSolver
from GridPlayers.GridPuzzle.GridPuzzleMirukutiTeasePlayer import GridPuzzleMirukutiTeasePlayer
from GridProviders.GridPuzzle.GridPuzzleMirukutiTeaseGridProvider import GridPuzzleMirukutiTeaseGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/mirukuti-tease",
        GridPuzzleMirukutiTeaseGridProvider,
        GridPuzzleMirukutiTeasePlayer
    )(MirukutiTeaseSolver)
