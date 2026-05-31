from PuzzleSolver.Puzzles.Usotatami.UsotatamiSolver import UsotatamiSolver
from GridPlayers.GridPuzzle.GridPuzzleUsotatamiPlayer import GridPuzzleUsotatamiPlayer
from GridProviders.GridPuzzle.GridPuzzleUsotatamiGridProvider import GridPuzzleUsotatamiGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://gridpuzzle\.com/usotatami/.*",
        GridPuzzleUsotatamiGridProvider,
        GridPuzzleUsotatamiPlayer
    )(UsotatamiSolver)
