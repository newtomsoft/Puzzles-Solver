from Domain.Puzzles.Wamuzu.WamazuSolver import WamazuSolver
from GridPlayers.GridPuzzle.GridPuzzleWamazuPlayer import GridPuzzleWamazuPlayer
from GridProviders.GridPuzzle.GridPuzzleWamazuGridProvider import GridPuzzleWamazuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/wamuzu", 
        GridPuzzleWamazuGridProvider, 
        GridPuzzleWamazuPlayer
    )(WamazuSolver)