from Domain.Puzzles.Slant.SlantSolver import SlantSolver
from GridPlayers.PuzzleMobiles.PuzzleSlantPlayer import PuzzleSlantPlayer
from GridProviders.PuzzlesMobile.PuzzleSlantGridProvider import PuzzleSlantGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzles-mobile\.com/slant/.*",
        PuzzleSlantGridProvider,
        PuzzleSlantPlayer
    )(SlantSolver)
