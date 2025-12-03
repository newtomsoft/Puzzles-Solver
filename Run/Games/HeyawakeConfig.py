from Domain.Puzzles.Heyawake.HeyawakeSolver import HeyawakeSolver
from GridPlayers.PuzzleMobiles.PuzzleHeyawakePlayer import PuzzleHeyawakePlayer
from GridProviders.PuzzlesMobile.PuzzleHeyawakeGridProvider import PuzzleHeyawakeGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-heyawake\.com", 
        PuzzleHeyawakeGridProvider, 
        PuzzleHeyawakePlayer
    )(HeyawakeSolver)