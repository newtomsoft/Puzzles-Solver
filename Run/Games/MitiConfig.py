
from Domain.Puzzles.Miti.MitiSolver import MitiSolver
from GridPlayers.GridPuzzle.GridPuzzleMitiPlayer import GridPuzzleMitiPlayer
from GridProviders.GridPuzzle.GridPuzzleMitiGridProvider import GridPuzzleMitiGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/miti", 
        GridPuzzleMitiGridProvider, 
        GridPuzzleMitiPlayer
    )(MitiSolver)
