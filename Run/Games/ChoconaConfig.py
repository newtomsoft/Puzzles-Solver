from Domain.Puzzles.Chocona.ChoconaSolver import ChoconaSolver
from GridPlayers.GridPuzzle.GridPuzzleChoconaPlayer import GridPuzzleChoconaPlayer
from GridProviders.GridPuzzle.GridPuzzleChoconaGridProvider import GridPuzzleChoconaGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/chocona", 
        GridPuzzleChoconaGridProvider, 
        GridPuzzleChoconaPlayer
    )(ChoconaSolver)