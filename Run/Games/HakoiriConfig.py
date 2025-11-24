from Domain.Puzzles.Hakoiri.HakoiriSolver import HakoiriSolver
from GridPlayers.GridPuzzle.GridPuzzleHakoiriPlayer import GridPuzzleHakoiriPlayer
from GridProviders.GridPuzzle.GridPuzzleHakoiriGridProvider import GridPuzzleHakoiriGridProvider
from Run.GameRegistry import GameRegistry


def register_hakoiri():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/hakoiri", 
        GridPuzzleHakoiriGridProvider, 
        GridPuzzleHakoiriPlayer
    )(HakoiriSolver)