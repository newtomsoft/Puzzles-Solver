from Domain.Puzzles.Shakashaka.ShakashakaSolver import ShakashakaSolver
from GridPlayers.PuzzleMobiles.PuzzleShakashakaPlayer import PuzzleShakashakaPlayer
from GridProviders.PuzzlesMobile.PuzzleShakashakaGridProvider import PuzzleShakashakaGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register_game('shakashaka', ShakashakaSolver, PuzzleShakashakaGridProvider, PuzzleShakashakaPlayer)
