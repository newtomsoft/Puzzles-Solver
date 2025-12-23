from Domain.Puzzles.Bimaru.BimaruSolver import BimaruSolver
from GridPlayers.PuzzlesMobile.PuzzleBimaruPlayer import PuzzleBimaruPlayer
from GridProviders.PuzzlesMobile.PuzzleBimaruGridProvider import PuzzleBimaruGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-battleships\.com", 
        PuzzleBimaruGridProvider, 
        PuzzleBimaruPlayer
    )(BimaruSolver)