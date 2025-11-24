from Domain.Puzzles.Masyu.MasyuSolver import MasyuSolver
from GridPlayers.GridPuzzle.GridPuzzleMasyuPlayer import GridPuzzleMasyuPlayer
from GridPlayers.PuzzleMobiles.PuzzleMasyuPlayer import PuzzleMasyuPlayer
from GridProviders.GridPuzzle.GridPuzzleMasyuGridProvider import GridPuzzleMasyuGridProvider
from GridProviders.PuzzlesMobile.PuzzleMasyuGridProvider import PuzzleMasyuGridProvider
from Run.GameRegistry import GameRegistry


def register_masyu():
    GameRegistry.register_game(
        r"https://.*\.puzzle-masyu\.com", 
        PuzzleMasyuGridProvider, 
        PuzzleMasyuPlayer
    )(MasyuSolver)

    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/masyu", 
        GridPuzzleMasyuGridProvider, 
        GridPuzzleMasyuPlayer
    )(MasyuSolver)