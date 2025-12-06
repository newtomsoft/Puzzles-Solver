from Domain.Puzzles.Kanjo.KanjoSolver import KanjoSolver
from GridPlayers.GridPuzzle.GridPuzzleKanjoPlayer import GridPuzzleKanjoPlayer
from GridProviders.GridPuzzle.GridPuzzleKanjoGridProvider import GridPuzzleKanjoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/kanjo", 
        GridPuzzleKanjoGridProvider, 
        GridPuzzleKanjoPlayer
    )(KanjoSolver)