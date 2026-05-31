from PuzzleSolver.Puzzles.Kurotto.KurottoSolver import KurottoSolver
from GridPlayers.GridPuzzle.GridPuzzleKurottoPlayer import GridPuzzleKurottoPlayer
from GridProviders.GridPuzzle.GridPuzzleKurottoGridProvider import GridPuzzleKurottoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/kurotto",
        GridPuzzleKurottoGridProvider,
        GridPuzzleKurottoPlayer
    )(KurottoSolver)
