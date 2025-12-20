from Domain.Puzzles.Hitori.HitoriSolver import HitoriSolver
from GridPlayers.PuzzleMobiles.PuzzleHitoriPlayer import PuzzleHitoriPlayer
from GridPlayers.Vuqq.VuqqHitoriPlayer import VuqqHitoriPlayer
from GridProviders.PuzzlesMobile.PuzzleHitoriGridProvider import PuzzleHitoriGridProvider
from GridProviders.Vuqq.VuqqHitoriGridProvider import VuqqHitoriGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-hitori\.com", 
        PuzzleHitoriGridProvider, 
        PuzzleHitoriPlayer
    )(HitoriSolver)

    GameRegistry.register(
        r"https://vuqq\.com/.*hitori/.*",
        VuqqHitoriGridProvider,
        VuqqHitoriPlayer
    )(HitoriSolver)