from Domain.Puzzles.Hidoku.HidokuSolver import HidokuSolver
from GridPlayers.GridGames.HidokuPlayer import HidokuPlayer
from GridProviders.GridGames.HidokuGridProvider import HidokuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://gridgames.app/hidoku",
        HidokuGridProvider,
        HidokuPlayer
    )(HidokuSolver)
