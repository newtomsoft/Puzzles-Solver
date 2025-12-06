from Domain.Puzzles.Tasukuea.TasukueaSolver import TasukueaSolver
from GridPlayers.GridPuzzle.GridPuzzleTasukueaPlayer import GridPuzzleTasukueaPlayer
from GridProviders.GridPuzzle.GridPuzzleTasukueaGridProvider import GridPuzzleTasukueaGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/tasukuea", 
        GridPuzzleTasukueaGridProvider, 
        GridPuzzleTasukueaPlayer
    )(TasukueaSolver)