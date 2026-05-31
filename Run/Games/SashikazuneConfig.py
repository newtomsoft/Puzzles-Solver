from PuzzleSolver.Puzzles.Sashikazune.SashikazuneSolver import SashikazuneSolver
from GridProviders.GridPuzzle.GridPuzzleSashikazuneGridProvider import GridPuzzleSashikazuneGridProvider
from GridPlayers.GridPuzzle.GridPuzzleSashikazunePlayer import GridPuzzleSashikazunePlayer
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/sashikazune",
        GridPuzzleSashikazuneGridProvider,
        GridPuzzleSashikazunePlayer
    )(SashikazuneSolver)
