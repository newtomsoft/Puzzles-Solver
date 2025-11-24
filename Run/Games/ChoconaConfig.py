from Domain.Puzzles.Chocona.ChoconaSolver import ChoconaSolver
from GridPlayers.GridPuzzle.GridPuzzleChoconaPlayer import GridPuzzleChoconaPlayer
from GridProviders.GridPuzzle.GridPuzzleChoconaGridProvider import GridPuzzleChoconaGridProvider
from Run.GameRegistry import GameRegistry


def register_chocona():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/chocona", 
        GridPuzzleChoconaGridProvider, 
        GridPuzzleChoconaPlayer
    )(ChoconaSolver)