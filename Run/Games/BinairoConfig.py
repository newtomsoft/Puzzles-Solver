from Domain.Puzzles.Binairo.BinairoSolver import BinairoSolver
from GridPlayers.PuzzleMobiles.PuzzleBinairoPlayer import PuzzleBinairoPlayer
from GridProviders.PuzzlesMobile.PuzzleBinairoPlusGridProvider import PuzzleBinairoPlusGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-binairo\.com",
        PuzzleBinairoPlusGridProvider,
        PuzzleBinairoPlayer
    )(BinairoSolver)