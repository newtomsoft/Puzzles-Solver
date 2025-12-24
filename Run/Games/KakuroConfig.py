from Domain.Puzzles.Kakuro.KakuroSolver import KakuroSolver
from GridPlayers.PuzzlesMobile.PuzzleKakuroPlayer import PuzzleKakuroPlayer
from GridProviders.PuzzlesMobile.PuzzleKakuroGridProvider import PuzzleKakuroGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-kakuro\.com", 
        PuzzleKakuroGridProvider, 
        PuzzleKakuroPlayer
    )(KakuroSolver)
