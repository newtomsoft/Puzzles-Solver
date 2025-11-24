from Domain.Puzzles.Shingoki.ShingokiSolver import ShingokiSolver
from GridPlayers.GridPuzzle.GridPuzzleShingokiPlayer import GridPuzzleShingokiPlayer
from GridPlayers.PuzzleMobiles.PuzzleMasyuPlayer import PuzzleMasyuPlayer
from GridProviders.GridPuzzle.GridPuzzleShingokiGridProvider import GridPuzzleShingokiGridProvider
from GridProviders.PuzzlesMobile.PuzzleShingokiGridProvider import PuzzleShingokiGridProvider
from Run.GameRegistry import GameRegistry


def register_shingoki():
    # Puzzle Shingoki (uses Masyu player)
    GameRegistry.register_game(
        r"https://.*\.puzzle-shingoki\.com", 
        PuzzleShingokiGridProvider, 
        PuzzleMasyuPlayer
    )(ShingokiSolver)

    # Grid Puzzle Traffic Lights
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/traffic-lights", 
        GridPuzzleShingokiGridProvider, 
        GridPuzzleShingokiPlayer
    )(ShingokiSolver)


