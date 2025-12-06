from Domain.Puzzles.From1ToX.From1ToXSolver import From1ToXSolver
from GridPlayers.GridPuzzle.GridPuzzleFrom1ToXPlayer import GridPuzzleFrom1ToXPlayer
from GridProviders.GridPuzzle.GridPuzzleFrom1ToXGridProvider import GridPuzzleFrom1ToXGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/from1tox", 
        GridPuzzleFrom1ToXGridProvider, 
        GridPuzzleFrom1ToXPlayer
    )(From1ToXSolver)