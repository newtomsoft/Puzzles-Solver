from Domain.Puzzles.Kakurasu.KakurasuSolver import KakurasuSolver
from GridPlayers.PuzzleMobiles.PuzzleKakurasuPlayer import PuzzleKakurasuPlayer
from GridProviders.PuzzlesMobile.PuzzleKakurasuGridProvider import PuzzleKakurasuGridProvider
from Run.GameRegistry import GameRegistry


def register_kakurasu():
    GameRegistry.register_game(
        r"https://.*\.puzzle-kakurasu\.com", 
        PuzzleKakurasuGridProvider, 
        PuzzleKakurasuPlayer
    )(KakurasuSolver)