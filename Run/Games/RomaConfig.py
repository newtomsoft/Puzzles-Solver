from PuzzleSolver.Puzzles.Roma.RomaSolver import RomaSolver
from GridProviders.PuzzLink.PuzzLinkRomaGridProvider import PuzzLinkRomaGridProvider
from GridPlayers.PuzzLink.PuzzLinkRomaPlayer import PuzzLinkRomaPlayer
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*puzz\.link/.*roma",
        PuzzLinkRomaGridProvider,
        PuzzLinkRomaPlayer
    )(RomaSolver)
