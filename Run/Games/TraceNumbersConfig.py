from PuzzleSolver.Puzzles.TraceNumbers.TraceNumbersSolver import TraceNumbersSolver
from GridPlayers.GridPuzzle.GridPuzzleTraceNumbersPlayer import GridPuzzleTraceNumbersPlayer
from GridProviders.GridPuzzle.GridPuzzleTraceNumbersGridProvider import GridPuzzleTraceNumbersGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/trace-numbers",
        GridPuzzleTraceNumbersGridProvider,
        GridPuzzleTraceNumbersPlayer
    )(TraceNumbersSolver)
