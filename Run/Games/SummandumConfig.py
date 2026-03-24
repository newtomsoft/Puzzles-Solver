from Domain.Puzzles.Summandum.SummandumSolver import SummandumSolver
from GridPlayers.GridPuzzle.GridPuzzleSummandumPlayer import GridPuzzleSummandumPlayer
from GridProviders.GridPuzzle.GridPuzzleSummandumGridProvider import GridPuzzleSummandumGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/summandum",
        GridPuzzleSummandumGridProvider,
        GridPuzzleSummandumPlayer
    )(SummandumSolver)
