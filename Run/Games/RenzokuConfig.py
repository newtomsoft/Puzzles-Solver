from Domain.Puzzles.Renzoku.RenzokuSolver import RenzokuSolver
from GridPlayers.PuzzleMobiles.PuzzleFutoshikiPlayer import PuzzleFutoshikiPlayer
from GridProviders.PuzzlesMobile.PuzzleRenzokuGridProvider import PuzzleRenzokuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-futoshiki\.com/.*renzoku", 
        PuzzleRenzokuGridProvider, 
        PuzzleFutoshikiPlayer
    )(RenzokuSolver)