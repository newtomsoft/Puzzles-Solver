from Domain.Puzzles.Putteria.PutteriaSolver import PutteriaSolver
from GridPlayers.GridPuzzle.GridPuzzlePutteriaPlayer import GridPuzzlePutteriaPlayer
from GridProviders.GridPuzzle.GridPuzzlePutteriaGridProvider import GridPuzzlePutteriaGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/putteria",
        GridPuzzlePutteriaGridProvider,
        GridPuzzlePutteriaPlayer
    )(PutteriaSolver)
