from Domain.Puzzles.Geradeweg.GeradewegSolver import GeradewegSolver
from GridPlayers.GridPuzzle.GridPuzzleGeradewegPlayer import GridPuzzleGeradewegPlayer
from GridProviders.GridPuzzle.GridPuzzleGeradewegGridProvider import GridPuzzleGeradewegGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/straight-loop", 
        GridPuzzleGeradewegGridProvider, 
        GridPuzzleGeradewegPlayer
    )(GeradewegSolver)