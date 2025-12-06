from Domain.Puzzles.Nurikabe.NurikabeSolver import NurikabeSolver
from GridPlayers.PuzzleMobiles.PuzzleNurikabePlayer import PuzzleNurikabePlayer
from GridProviders.PuzzlesMobile.PuzzleNurikabeGridProvider import PuzzleNurikabeGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-nurikabe\.com", 
        PuzzleNurikabeGridProvider, 
        PuzzleNurikabePlayer
    )(NurikabeSolver)