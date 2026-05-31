from PuzzleSolver.Puzzles.Irasuto.IrasutoSolver import IrasutoSolver
from GridPlayers.GridPuzzle.GridPuzzleIrasutoPlayer import GridPuzzleIrasutoPlayer
from GridProviders.GridPuzzle.GridPuzzleIrasutoGridProvider import GridPuzzleIrasutoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/irasuto",
        GridPuzzleIrasutoGridProvider,
        GridPuzzleIrasutoPlayer
    )(IrasutoSolver)
