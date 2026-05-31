from PuzzleSolver.Puzzles.KohiGyunyu.KohiGyunyuSolver import KohiGyunyuSolver
from GridPlayers.GridPuzzle.GridPuzzleKohiGyunyuPlayer import GridPuzzleKohiGyunyuPlayer
from GridProviders.GridPuzzle.GridPuzzleKohiGyunyuGridProvider import GridPuzzleKohiGyunyuGridProvider
from Run.GameRegistry import GameRegistry

def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/kohi-gyunyu",
        GridPuzzleKohiGyunyuGridProvider,
        GridPuzzleKohiGyunyuPlayer
    )(KohiGyunyuSolver)
