from Domain.Puzzles.Bimaru.BimaruSolver import BimaruSolver
from GridPlayers.PuzzleMobiles.PuzzleBimaruPlayer import PuzzleBimaruPlayer
from GridProviders.PuzzlesMobile.PuzzleBimaruGridProvider import PuzzleBimaruGridProvider
from Run.GameRegistry import GameRegistry


def register_bimaru():
    GameRegistry.register_game(
        r"https://.*\.puzzle-battleships\.com", 
        PuzzleBimaruGridProvider, 
        PuzzleBimaruPlayer
    )(BimaruSolver)