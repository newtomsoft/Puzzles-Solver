from PuzzleSolver.Puzzles.Binairo.BinairoSolver import BinairoSolver
from GridPlayers.GridPuzzle.GridPuzzleBinairoPlayer import GridPuzzleBinairoPlayer
from GridPlayers.PuzzlesMobile.PuzzleBinairoPlayer import PuzzleBinairoPlayer
from GridProviders.GridPuzzle.GridPuzzleBinairoGridProvider import GridPuzzleBinairoGridProvider
from GridProviders.PuzzlesMobile.PuzzleBinairoGridProvider import PuzzleBinairoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/binairo",
        GridPuzzleBinairoGridProvider,
        GridPuzzleBinairoPlayer
    )(BinairoSolver)

    GameRegistry.register(
        r"https://.*\.puzzle-binairo\.com",
        PuzzleBinairoGridProvider,
        PuzzleBinairoPlayer
    )(BinairoSolver)