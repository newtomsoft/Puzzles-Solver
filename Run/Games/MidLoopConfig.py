from Domain.Puzzles.MidLoop.MidLoopSolver import MidLoopSolver
from GridPlayers.GridPuzzle.GridPuzzleMidLoopPlayer import GridPuzzleMidLoopPlayer
from GridProviders.GridPuzzle.GridPuzzleMidLoopGridProvider import GridPuzzleMidLoopGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/mid-loop", 
        GridPuzzleMidLoopGridProvider, 
        GridPuzzleMidLoopPlayer
    )(MidLoopSolver)