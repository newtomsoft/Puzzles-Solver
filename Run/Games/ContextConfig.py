from PuzzleSolver.Puzzles.Context.ContextSolver import ContextSolver
from GridPlayers.GridPuzzle.GridPuzzleContextPlayer import GridPuzzleContextPlayer
from GridPlayers.PuzzLink.PuzzLinkContextPlayer import PuzzLinkContextPlayer
from GridProviders.GridPuzzle.GridPuzzleContextGridProvider import GridPuzzleContextGridProvider
from GridProviders.PuzzLink.PuzzLinkContextGridProvider import PuzzLinkContextGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/context",
        GridPuzzleContextGridProvider,
        GridPuzzleContextPlayer
    )(ContextSolver)

    GameRegistry.register(
        r"https://.*puzz\.link/.*context",
        PuzzLinkContextGridProvider,
        PuzzLinkContextPlayer
    )(ContextSolver)
