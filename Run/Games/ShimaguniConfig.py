from Domain.Puzzles.Shimaguni.ShimaguniSolver import ShimaguniSolver
from GridPlayers.GridPuzzle.GridPuzzleShimaguniPlayer import GridPuzzleShimaguniPlayer
from GridProviders.GridPuzzle.GridPuzzleShimaguniGridProvider import GridPuzzleShimaguniGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/shimaguni", 
        GridPuzzleShimaguniGridProvider, 
        GridPuzzleShimaguniPlayer
    )(ShimaguniSolver)
