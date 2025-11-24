from Domain.Puzzles.Futoshiki.FutoshikiSolver import FutoshikiSolver
from GridPlayers.PuzzleMobiles.PuzzleFutoshikiPlayer import PuzzleFutoshikiPlayer
from GridProviders.PuzzlesMobile.PuzzleFutoshikiGridProvider import PuzzleFutoshikiGridProvider
from Run.GameRegistry import GameRegistry


def register_futoshiki():
    GameRegistry.register_game(
        r"https://.*\.puzzle-futoshiki\.com", 
        PuzzleFutoshikiGridProvider, 
        PuzzleFutoshikiPlayer
    )(FutoshikiSolver)