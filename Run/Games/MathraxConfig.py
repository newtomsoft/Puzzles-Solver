from PuzzleSolver.Puzzles.Mathrax.MathraxSolver import MathraxSolver
from GridPlayers.GridPuzzle.GridPuzzleMathraxPlayer import GridPuzzleMathraxPlayer
from GridProviders.GridPuzzle.GridPuzzleMathraxGridProvider import GridPuzzleMathraxGridProvider
from Run.GameRegistry import GameRegistry

def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/mathrax(-plus)?",
        GridPuzzleMathraxGridProvider,
        GridPuzzleMathraxPlayer
    )(MathraxSolver)
