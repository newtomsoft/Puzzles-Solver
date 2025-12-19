from Domain.Puzzles.Kakuro.KakuroSolver import KakuroSolver
from GridPlayers.Vuqq.VuqqKakuroPlayer import VuqqKakuroPlayer
from GridProviders.PuzzlesMobile.PuzzleKakuroGridProvider import PuzzleKakuroGridProvider
from GridProviders.Vuqq.VuqqKakuroGridProvider import VuqqKakuroGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-kakuro\.com", 
        PuzzleKakuroGridProvider, 
        PuzzleKakuroPlayer
    )(KakuroSolver)

    GameRegistry.register(
        r"https://vuqq\.com/.*/kakuro/",
        VuqqKakuroGridProvider,
        VuqqKakuroPlayer
    )(KakuroSolver)
