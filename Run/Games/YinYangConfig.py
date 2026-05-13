from Domain.Puzzles.YinYang.YinYangSolver import YinYangSolver
from GridPlayers.GridPuzzle.GridPuzzleYinYangPlayer import GridPuzzleYinYangPlayer
from GridPlayers.PuzzlesMobile.PuzzleBinairoPlayer import PuzzleBinairoPlayer
from GridProviders.GridPuzzle.GridPuzzleYinYangGridProvider import GridPuzzleYinYangGridProvider
from GridProviders.PuzzlesMobile.PuzzleYinYangGridProvider import PuzzleYinYangGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-yin-yang\.com", 
        PuzzleYinYangGridProvider, 
        PuzzleBinairoPlayer
    )(YinYangSolver)

    GameRegistry.register(
        r"https://.*gridpuzzle\.com/.*yinyang",
        GridPuzzleYinYangGridProvider,
        GridPuzzleYinYangPlayer
    )(YinYangSolver)
