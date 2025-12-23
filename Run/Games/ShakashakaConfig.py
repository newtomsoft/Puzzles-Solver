from Domain.Puzzles.Shakashaka.ShakashakaSolver import ShakashakaSolver
from GridPlayers.PuzzlesMobile.PuzzleShakashakaPlayer import PuzzleShakashakaPlayer
from GridProviders.PuzzlesMobile.PuzzleShakashakaGridProvider import PuzzleShakashakaGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-shakashaka\.com",
        PuzzleShakashakaGridProvider,
        PuzzleShakashakaPlayer
    )(ShakashakaSolver)