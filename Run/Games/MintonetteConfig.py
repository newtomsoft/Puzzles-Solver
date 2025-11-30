from Domain.Puzzles.Mintonette.MintonetteSolver_or_tools import MintonetteSolver
from GridPlayers.GridPuzzle.GridPuzzleMintonettePlayer import GridPuzzleMintonettePlayer
from GridProviders.GridPuzzle.GridPuzzleMintonetteGridProvider import GridPuzzleMintonetteGridProvider
from Run.GameRegistry import GameRegistry


def register_mintonette():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/mintonette", 
        GridPuzzleMintonetteGridProvider, 
        GridPuzzleMintonettePlayer
    )(MintonetteSolver)
