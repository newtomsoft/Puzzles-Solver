from PuzzleSolver.Puzzles.Kazoku.KazokuSolver import KazokuSolver
from GridPlayers.GridPuzzle.GridPuzzleKazokuPlayer import GridPuzzleKazokuPlayer
from GridProviders.GridPuzzle.GridPuzzleKazokuGridProvider import GridPuzzleKazokuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/kazoku.*", 
        GridPuzzleKazokuGridProvider, 
        GridPuzzleKazokuPlayer
    )(KazokuSolver)
