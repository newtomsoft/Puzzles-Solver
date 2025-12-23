from Domain.Puzzles.Binairo.BinairoSolver import BinairoSolver
from GridPlayers.PuzzlesMobile.PuzzleBinairoPlayer import PuzzleBinairoPlayer
from GridProviders.PuzzlesMobile.PuzzleBinairoGridProvider import PuzzleBinairoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-binairo\.com",
        PuzzleBinairoGridProvider,
        PuzzleBinairoPlayer
    )(BinairoSolver)