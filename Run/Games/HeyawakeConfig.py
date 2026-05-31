from PuzzleSolver.Puzzles.Heyawake.HeyawakeSolver import HeyawakeSolver
from GridPlayers.GridPuzzle.GridPuzzleHeyawakePlayer import GridPuzzleHeyawakePlayer
from GridPlayers.PuzzlesMobile.PuzzleHeyawakePlayer import PuzzleHeyawakePlayer
from GridProviders.GridPuzzle.GridPuzzleHeyawakeGridProvider import GridPuzzleHeyawakeGridProvider
from GridProviders.PuzzlesMobile.PuzzleHeyawakeGridProvider import PuzzleHeyawakeGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/heyawake",
        GridPuzzleHeyawakeGridProvider,
        GridPuzzleHeyawakePlayer
    )(HeyawakeSolver)

    GameRegistry.register(
        r"https://.*\.puzzle-heyawake\.com",
        PuzzleHeyawakeGridProvider,
        PuzzleHeyawakePlayer
    )(HeyawakeSolver)
