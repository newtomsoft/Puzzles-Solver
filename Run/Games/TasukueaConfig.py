from Domain.Puzzles.Tasukuea.TasukueaSolver import TasukueaSolver
from GridPlayers.GridPuzzle.GridPuzzleTasukueaPlayer import GridPuzzleTasukueaPlayer
from GridProviders.GridPuzzle.GridPuzzleTasukueaGridProvider import GridPuzzleTasukueaGridProvider
from Run.GameRegistry import GameRegistry


def register_tasukuea():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/tasukuea", 
        GridPuzzleTasukueaGridProvider, 
        GridPuzzleTasukueaPlayer
    )(TasukueaSolver)