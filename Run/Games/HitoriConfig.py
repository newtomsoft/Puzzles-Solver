from Domain.Puzzles.Hitori.HitoriSolver import HitoriSolver
from GridPlayers.PuzzleMobiles.PuzzleHitoriPlayer import PuzzleHitoriPlayer
from GridProviders.PuzzlesMobile.PuzzleHitoriGridProvider import PuzzleHitoriGridProvider
from Run.GameRegistry import GameRegistry


def register_hitori():
    GameRegistry.register_game(
        r"https://.*\.puzzle-hitori\.com", 
        PuzzleHitoriGridProvider, 
        PuzzleHitoriPlayer
    )(HitoriSolver)