from Domain.Puzzles.Hiroimono.HiroimonoSolver import HiroimonoSolver
from GridPlayers.GridPuzzle.GridPuzzleHiroimonoPlayer import GridPuzzleHiroimonoPlayer
from GridProviders.GridPuzzle.GridPuzzleHiroimonoGridProvider import GridPuzzleHiroimonoGridProvider
from Run.GameRegistry import GameRegistry

def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/hiroimono",
        GridPuzzleHiroimonoGridProvider,
        GridPuzzleHiroimonoPlayer
    )(HiroimonoSolver)
