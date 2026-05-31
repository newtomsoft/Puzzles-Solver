from PuzzleSolver.Puzzles.Kuroshuto.KuroshutoSolver import KuroshutoSolver
from GridProviders.GridPuzzle.GridPuzzleKuroshutoGridProvider import GridPuzzleKuroshutoGridProvider
from GridPlayers.GridPuzzle.GridPuzzleKuroshutoPlayer import GridPuzzleKuroshutoPlayer
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/kuroshuto",
        GridPuzzleKuroshutoGridProvider,
        GridPuzzleKuroshutoPlayer
    )(KuroshutoSolver)