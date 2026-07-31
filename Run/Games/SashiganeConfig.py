from PuzzleSolver.Puzzles.Sashigane.SashiganeSolver import SashiganeSolver
from GridProviders.GridPuzzle.GridPuzzleSashiganeGridProvider import GridPuzzleSashiganeGridProvider
from GridProviders.PuzzLink.PuzzLinkSashiganeGridProvider import PuzzLinkSashiganeGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/sashigane",
        GridPuzzleSashiganeGridProvider,
        None
    )(SashiganeSolver)

    GameRegistry.register(
        r"https://.*puzz\.link/.*sashigane",
        PuzzLinkSashiganeGridProvider,
        None
    )(SashiganeSolver)
