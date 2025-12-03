from Domain.Puzzles.Futoshiki.FutoshikiSolver import FutoshikiSolver
from GridPlayers.PuzzleMobiles.PuzzleFutoshikiPlayer import PuzzleFutoshikiPlayer
from GridProviders.PuzzlesMobile.PuzzleFutoshikiGridProvider import PuzzleFutoshikiGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-futoshiki\.com", 
        PuzzleFutoshikiGridProvider, 
        PuzzleFutoshikiPlayer
    )(FutoshikiSolver)