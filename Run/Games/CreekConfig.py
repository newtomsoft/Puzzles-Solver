from Domain.Puzzles.Creek.CreekSolver import CreekSolver
from GridPlayers.GridPuzzle.GridPuzzleCreekPlayer import GridPuzzleCreekPlayer
from GridProviders.GridPuzzle.GridPuzzleCreekGridProvider import GridPuzzleCreekGridProvider
from Run.GameRegistry import GameRegistry


def register_creek():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/creek", 
        GridPuzzleCreekGridProvider, 
        GridPuzzleCreekPlayer
    )(CreekSolver)