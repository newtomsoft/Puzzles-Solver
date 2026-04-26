from Domain.Puzzles.Nuribou.NuribouSolver import NuribouSolver
from GridPlayers.GridPuzzle.GridPuzzleNuribouPlayer import GridPuzzleNuribouPlayer
from GridProviders.GridPuzzle.GridPuzzleNuribouGridProvider import GridPuzzleNuribouGridProvider
from Run.GameRegistry import GameRegistry

def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/nuribou", 
        GridPuzzleNuribouGridProvider, 
        GridPuzzleNuribouPlayer
    )(NuribouSolver)
