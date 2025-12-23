from Domain.Puzzles.Shingoki.ShingokiSolver import ShingokiSolver
from GridPlayers.GridPuzzle.GridPuzzleShingokiPlayer import GridPuzzleShingokiPlayer
from GridPlayers.PuzzlesMobile.PuzzleMasyuPlayer import PuzzleMasyuPlayer
from GridProviders.GridPuzzle.GridPuzzleShingokiGridProvider import GridPuzzleShingokiGridProvider
from GridProviders.PuzzlesMobile.PuzzleShingokiGridProvider import PuzzleShingokiGridProvider
from Run.GameRegistry import GameRegistry


def register():
    # Puzzle Shingoki (uses Masyu player)
    GameRegistry.register(
        r"https://.*\.puzzle-shingoki\.com", 
        PuzzleShingokiGridProvider, 
        PuzzleMasyuPlayer
    )(ShingokiSolver)

    # Grid Puzzle Traffic Lights
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/traffic-lights", 
        GridPuzzleShingokiGridProvider, 
        GridPuzzleShingokiPlayer
    )(ShingokiSolver)


