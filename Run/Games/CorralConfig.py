from PuzzleSolver.Puzzles.Corral.CorralSolver import CorralSolver
from GridPlayers.GridPuzzle.GridPuzzleCorralPlayer import GridPuzzleCorralPlayer
from GridProviders.GridPuzzle.GridPuzzleCorralGridProvider import GridPuzzleCorralGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/cave.*",
        GridPuzzleCorralGridProvider,
        GridPuzzleCorralPlayer
    )(CorralSolver)
