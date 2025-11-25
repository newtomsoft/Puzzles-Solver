from Domain.Puzzles.Nurikabe.NurikabeSolver import NurikabeSolver
from GridPlayers.PuzzleMobiles.PuzzleNurikabePlayer import PuzzleNurikabePlayer
from GridProviders.PuzzlesMobile.PuzzleNurikabeGridProvider import PuzzleNurikabeGridProvider
from Run.GameRegistry import GameRegistry


def register_nurikabe():
    GameRegistry.register_game(
        r"https://.*\.puzzle-nurikabe\.com", 
        PuzzleNurikabeGridProvider, 
        PuzzleNurikabePlayer
    )(NurikabeSolver)