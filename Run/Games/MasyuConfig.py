from Domain.Puzzles.Masyu.MasyuSolver import MasyuSolver
from GridPlayers.GridPuzzle.GridPuzzleMasyuPlayer import GridPuzzleMasyuPlayer
from GridPlayers.PuzzleMobiles.PuzzleMasyuPlayer import PuzzleMasyuPlayer
from GridProviders.GridPuzzle.GridPuzzleMasyuGridProvider import GridPuzzleMasyuGridProvider
from GridProviders.PuzzlesMobile.PuzzleMasyuGridProvider import PuzzleMasyuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-masyu\.com", 
        PuzzleMasyuGridProvider, 
        PuzzleMasyuPlayer
    )(MasyuSolver)

    GameRegistry.register(
        r"https://.*gridpuzzle\.com/masyu", 
        GridPuzzleMasyuGridProvider, 
        GridPuzzleMasyuPlayer
    )(MasyuSolver)