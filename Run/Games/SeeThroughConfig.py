from Domain.Puzzles.SeeThrough.SeeThroughSolver import SeeThroughSolver
from GridPlayers.GridPuzzle.GridPuzzleSeeThroughPlayer import GridPuzzleSeeThroughPlayer
from GridProviders.GridPuzzle.GridPuzzleSeeThroughGridProvider import GridPuzzleSeeThroughGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/seethrough", 
        GridPuzzleSeeThroughGridProvider, 
        GridPuzzleSeeThroughPlayer
    )(SeeThroughSolver)