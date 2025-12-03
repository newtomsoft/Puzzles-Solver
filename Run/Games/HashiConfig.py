from Domain.Puzzles.Hashi.HashiSolver import HashiSolver
from GridPlayers.GridPuzzle.GridPuzzleHashiPlayer import GridPuzzleHashiPlayer
from GridPlayers.PuzzleMobiles.PuzzleHashiPlayer import PuzzleHashiPlayer
from GridProviders.GridPuzzle.GridPuzzleHashiGridProvider import GridPuzzleHashiGridProvider
from GridProviders.PuzzlesMobile.PuzzleHashiGridProvider import PuzzleHashiGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-bridges\.com", 
        PuzzleHashiGridProvider, 
        PuzzleHashiPlayer
    )(HashiSolver)

    GameRegistry.register(
        r"https://.*gridpuzzle\.com/bridges", 
        GridPuzzleHashiGridProvider, 
        GridPuzzleHashiPlayer
    )(HashiSolver)