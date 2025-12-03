from Domain.Puzzles.Hakoiri.HakoiriSolver import HakoiriSolver
from GridPlayers.GridPuzzle.GridPuzzleHakoiriPlayer import GridPuzzleHakoiriPlayer
from GridProviders.GridPuzzle.GridPuzzleHakoiriGridProvider import GridPuzzleHakoiriGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/hakoiri", 
        GridPuzzleHakoiriGridProvider, 
        GridPuzzleHakoiriPlayer
    )(HakoiriSolver)