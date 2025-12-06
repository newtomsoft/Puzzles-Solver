from Domain.Puzzles.Nanro.NanroSolver import NanroSolver
from GridPlayers.GridPuzzle.GridPuzzleNanroPlayer import GridPuzzleNanroPlayer
from GridProviders.GridPuzzle.GridPuzzleNanroGridProvider import GridPuzzleNanroGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/nanro", 
        GridPuzzleNanroGridProvider, 
        GridPuzzleNanroPlayer
    )(NanroSolver)