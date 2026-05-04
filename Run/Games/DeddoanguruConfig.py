from Domain.Puzzles.Deddoanguru.DeddoanguruSolver import DeddoanguruSolver
from GridPlayers.GridPuzzle.GridPuzzleDeddoanguruPlayer import GridPuzzleDeddoanguruPlayer
from GridProviders.GridPuzzle.GridPuzzleDeddoanguruGridProvider import GridPuzzleDeddoanguruGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/deddoanguru",
        GridPuzzleDeddoanguruGridProvider,
        GridPuzzleDeddoanguruPlayer
    )(DeddoanguruSolver)
