from Domain.Puzzles.Fobidoshi.FobidoshiSolver import FobidoshiSolver
from GridPlayers.GridPuzzle.GridPuzzleFobidoshiPlayer import GridPuzzleFobidoshiPlayer
from GridProviders.GridPuzzle.GridPuzzleFobidoshiGridProvider import GridPuzzleFobidoshiGridProvider
from Run.GameRegistry import GameRegistry


def register_fobidoshi():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/fobidoshi", 
        GridPuzzleFobidoshiGridProvider, 
        GridPuzzleFobidoshiPlayer
    )(FobidoshiSolver)