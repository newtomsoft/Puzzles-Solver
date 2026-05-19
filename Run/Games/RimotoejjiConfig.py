from Domain.Puzzles.Rimotoejji.RimotoejjiSolver import RimotoejjiSolver
from GridPlayers.GridPuzzle.GridPuzzleRimotoejjiPlayer import GridPuzzleRimotoejjiPlayer
from GridProviders.GridPuzzle.GridPuzzleRimotoejjiGridProvider import GridPuzzleRimotoejjiGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/rimotoejji",
        GridPuzzleRimotoejjiGridProvider,
        GridPuzzleRimotoejjiPlayer
    )(RimotoejjiSolver)
