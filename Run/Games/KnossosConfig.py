from Domain.Puzzles.Knossos.KnossosSolver import KnossosSolver
from GridPlayers.GridPuzzle.GridPuzzleKnossosPlayer import GridPuzzleKnossosPlayer
from GridProviders.GridPuzzle.GridPuzzleKnossosGridProvider import GridPuzzleKnossosGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/knossos",
        GridPuzzleKnossosGridProvider,
        GridPuzzleKnossosPlayer
    )(KnossosSolver)
