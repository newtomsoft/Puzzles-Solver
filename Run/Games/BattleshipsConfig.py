from Domain.Puzzles.Bimaru.BimaruSolver import BimaruSolver
from GridPlayers.GridPuzzle.GridPuzzleBattleshipsPlayer import GridPuzzleBattleshipsPlayer
from GridProviders.GridPuzzle.GridPuzzleBattleshipsGridProvider import GridPuzzleBattleshipsGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/battleships",
        GridPuzzleBattleshipsGridProvider,
        GridPuzzleBattleshipsPlayer
    )(BimaruSolver)
