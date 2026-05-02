from Domain.Puzzles.Buraitoraito.BuraitoraitoSolver import BuraitoraitoSolver
from GridPlayers.GridPuzzle.GridPuzzleBuraitoraitoPlayer import GridPuzzleBuraitoraitoPlayer
from GridProviders.GridPuzzle.GridPuzzleBuraitoraitoGridProvider import GridPuzzleBuraitoraitoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/bright-light/",
        GridPuzzleBuraitoraitoGridProvider,
        GridPuzzleBuraitoraitoPlayer
    )(BuraitoraitoSolver)
