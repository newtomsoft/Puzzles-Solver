from PuzzleSolver.Puzzles.Hanare.HanareSolver import HanareSolver
from GridPlayers.GridPuzzle.GridPuzzleHanarePlayer import GridPuzzleHanarePlayer
from GridProviders.GridPuzzle.GridPuzzleHanareGridProvider import GridPuzzleHanareGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/hanare",
        GridPuzzleHanareGridProvider,
        GridPuzzleHanarePlayer
    )(HanareSolver)
