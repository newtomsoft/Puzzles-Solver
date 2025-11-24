from Domain.Puzzles.Doppelblock.DoppelblockSolver import DoppelblockSolver
from GridPlayers.GridPuzzle.GridPuzzleDoppelblockPlayer import GridPuzzleDoppelblockPlayer
from GridProviders.GridPuzzle.GridPuzzleDoppelblockGridProvider import GridPuzzleDoppelblockGridProvider
from Run.GameRegistry import GameRegistry


def register_doppelblock():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/doppelblock", 
        GridPuzzleDoppelblockGridProvider, 
        GridPuzzleDoppelblockPlayer
    )(DoppelblockSolver)