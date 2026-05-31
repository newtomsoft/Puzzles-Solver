from Domain.Puzzles.Foseruzu.FoseruzuSolver import FoseruzuSolver
from GridPlayers.GridPuzzle.GridPuzzleFoseruzuPlayer import GridPuzzleFoseruzuPlayer
from GridProviders.GridPuzzle.GridPuzzleFoseruzuGridProvider import GridPuzzleFoseruzuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/foseruzu",
        GridPuzzleFoseruzuGridProvider,
        GridPuzzleFoseruzuPlayer
    )(FoseruzuSolver)
