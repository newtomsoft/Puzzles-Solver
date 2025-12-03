from Domain.Puzzles.NumberCross.NumberCrossSolver import NumberCrossSolver
from GridPlayers.GridPuzzle.GridPuzzleNumberCrossPlayer import GridPuzzleNumberCrossPlayer
from GridProviders.GridPuzzle.GridPuzzleNumberCrossGridProvider import GridPuzzleNumberCrossGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/number-cross", 
        GridPuzzleNumberCrossGridProvider, 
        GridPuzzleNumberCrossPlayer
    )(NumberCrossSolver)