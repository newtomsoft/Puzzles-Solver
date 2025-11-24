from Domain.Puzzles.Binairo.BinairoSolver import BinairoSolver
from GridPlayers.PuzzleMobiles.PuzzleBinairoPlayer import PuzzleBinairoPlayer
from GridProviders.PuzzlesMobile.PuzzleBinairoGridProvider import PuzzleBinairoGridProvider
from Run.GameRegistry import GameRegistry


def register_binairo():
    GameRegistry.register_game(
        r"https://.*\.puzzle-binairo\.com", 
        PuzzleBinairoGridProvider, 
        PuzzleBinairoPlayer
    )(BinairoSolver)