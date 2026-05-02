from Domain.Puzzles.ArrowWeb.ArrowWebSolver import ArrowWebSolver
from GridPlayers.GridPuzzle.GridPuzzleArrowWebPlayer import GridPuzzleArrowWebPlayer
from GridProviders.GridPuzzle.GridPuzzleArrowWebGridProvider import GridPuzzleArrowWebGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/arrow-web",
        GridPuzzleArrowWebGridProvider,
        GridPuzzleArrowWebPlayer
    )(ArrowWebSolver)
