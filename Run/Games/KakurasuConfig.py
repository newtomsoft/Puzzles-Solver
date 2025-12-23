from Domain.Puzzles.Kakurasu.KakurasuSolver import KakurasuSolver
from GridPlayers.PuzzlesMobile.PuzzleKakurasuPlayer import PuzzleKakurasuPlayer
from GridProviders.PuzzlesMobile.PuzzleKakurasuGridProvider import PuzzleKakurasuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-kakurasu\.com", 
        PuzzleKakurasuGridProvider, 
        PuzzleKakurasuPlayer
    )(KakurasuSolver)