from Domain.Puzzles.Hitori.HitoriSolver import HitoriSolver
from GridPlayers.PuzzleMobiles.PuzzleHitoriPlayer import PuzzleHitoriPlayer
from GridProviders.PuzzlesMobile.PuzzleHitoriGridProvider import PuzzleHitoriGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-hitori\.com", 
        PuzzleHitoriGridProvider, 
        PuzzleHitoriPlayer
    )(HitoriSolver)