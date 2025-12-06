from Domain.Puzzles.BorderBlock.BorderBlockSolver import BorderBlockSolver
from GridPlayers.GridPuzzle.GridPuzzleBorderBlockPlayer import GridPuzzleBorderBlockPlayer
from GridProviders.GridPuzzle.GridPuzzleBorderBlockGridProvider import GridPuzzleBorderBlockGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/bodaburokku",
        GridPuzzleBorderBlockGridProvider,
        GridPuzzleBorderBlockPlayer
    )(BorderBlockSolver)
