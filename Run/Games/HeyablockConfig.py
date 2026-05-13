from Domain.Puzzles.Heyablock.HeyablockSolver import HeyablockSolver
from GridPlayers.GridPuzzle.GridPuzzleHeyablockPlayer import GridPuzzleHeyablockPlayer
from GridProviders.GridPuzzle.GridPuzzleHeyablockGridProvider import GridPuzzleHeyablockGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/heyablock",
        GridPuzzleHeyablockGridProvider,
        GridPuzzleHeyablockPlayer
    )(HeyablockSolver)
