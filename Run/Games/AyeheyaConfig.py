from PuzzleSolver.Puzzles.Ayeheya.AyeheyaSolver import AyeheyaSolver
from GridPlayers.PuzzLink.PuzzLinkAyeheyaPlayer import PuzzLinkAyeheyaPlayer
from GridProviders.PuzzLink.PuzzLinkAyeheyaGridProvider import PuzzLinkAyeheyaGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*puzz\.link/.*ayeheya",
        PuzzLinkAyeheyaGridProvider,
        PuzzLinkAyeheyaPlayer
    )(AyeheyaSolver)
