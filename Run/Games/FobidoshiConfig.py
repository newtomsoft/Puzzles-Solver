from Domain.Puzzles.Fobidoshi.FobidoshiSolver import FobidoshiSolver
from GridPlayers.GridPuzzle.GridPuzzleFobidoshiPlayer import GridPuzzleFobidoshiPlayer
from GridProviders.GridPuzzle.GridPuzzleFobidoshiGridProvider import GridPuzzleFobidoshiGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/fobidoshi", 
        GridPuzzleFobidoshiGridProvider, 
        GridPuzzleFobidoshiPlayer
    )(FobidoshiSolver)