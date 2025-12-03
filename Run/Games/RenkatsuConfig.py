from Domain.Puzzles.Renkatsu.RenkatsuSolver import RenkatsuSolver
from GridPlayers.GridPuzzle.GridPuzzleRenkatsuPlayer import GridPuzzleRenkatsuPlayer
from GridProviders.GridPuzzle.GridPuzzleRenkatsuGridProvider import GridPuzzleRenkatsuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/renkatsu", 
        GridPuzzleRenkatsuGridProvider, 
        GridPuzzleRenkatsuPlayer
    )(RenkatsuSolver)