from Domain.Puzzles.Tapa.TapaSolver import TapaSolver
from GridPlayers.PuzzleMobiles.PuzzleTapaPlayer import PuzzleTapaPlayer
from GridProviders.PuzzlesMobile.PuzzleTapaGridProvider import PuzzleTapaGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-tapa\.com", 
        PuzzleTapaGridProvider, 
        PuzzleTapaPlayer
    )(TapaSolver)