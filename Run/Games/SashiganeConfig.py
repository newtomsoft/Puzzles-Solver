from PuzzleSolver.Puzzles.Sashigane.SashiganeSolver import SashiganeSolver
from GridProviders.PuzzLink.PuzzLinkSashiganeGridProvider import PuzzLinkSashiganeGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*puzz\.link/.*sashigane",
        PuzzLinkSashiganeGridProvider,
        None
    )(SashiganeSolver)
