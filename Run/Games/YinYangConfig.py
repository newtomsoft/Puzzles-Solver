from Domain.Puzzles.YinYang.YinYangSolver import YinYangSolver
from GridPlayers.PuzzleMobiles.PuzzleBinairoPlayer import PuzzleBinairoPlayer
from GridProviders.PuzzlesMobile.PuzzleYinYangGridProvider import PuzzleYinYangGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-yin-yang\.com", 
        PuzzleYinYangGridProvider, 
        PuzzleBinairoPlayer
    )(YinYangSolver)