from Domain.Puzzles.KakuteruAnpu.KakuteruAnpuSolver import KakuteruAnpuSolver
from GridPlayers.GridPuzzle.GridPuzzleKakuteruAnpuPlayer import GridPuzzleKakuteruAnpuPlayer
from GridProviders.GridPuzzle.GridPuzzleKakuteruAnpuGridProvider import GridPuzzleKakuteruAnpuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/cocktail-lamp", 
        GridPuzzleKakuteruAnpuGridProvider, 
        GridPuzzleKakuteruAnpuPlayer
    )(KakuteruAnpuSolver)