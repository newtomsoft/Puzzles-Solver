from Domain.Puzzles.LookAir.LookAirSolver import LookAirSolver
from GridPlayers.GridPuzzle.GridPuzzleLookAirPlayer import GridPuzzleLookAirPlayer
from GridProviders.GridPuzzle.GridPuzzleLookAirGridProvider import GridPuzzleLookAirGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/look-air", 
        GridPuzzleLookAirGridProvider, 
        GridPuzzleLookAirPlayer
    )(LookAirSolver)