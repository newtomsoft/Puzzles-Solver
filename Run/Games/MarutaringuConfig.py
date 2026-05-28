from Domain.Puzzles.Marutaringu.MarutaringuSolver import MarutaringuSolver
from GridPlayers.GridPuzzle.GridPuzzleMarutaringuPlayer import GridPuzzleMarutaringuPlayer
from GridProviders.GridPuzzle.GridPuzzleMarutaringuGridProvider import GridPuzzleMarutaringuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/marutaringu",
        GridPuzzleMarutaringuGridProvider,
        GridPuzzleMarutaringuPlayer
    )(MarutaringuSolver)
