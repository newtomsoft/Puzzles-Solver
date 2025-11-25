from Domain.Puzzles.Yajikabe.YajilkabeSolver import YajikabeSolver
from GridPlayers.GridPuzzle.GridPuzzleYajikabePlayer import GridPuzzleYajikabePlayer
from GridProviders.GridPuzzle.GridPuzzleYajikabeGridProvider import GridPuzzleYajikabeGridProvider
from Run.GameRegistry import GameRegistry


def register_yajikabe():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/yajikabe", 
        GridPuzzleYajikabeGridProvider, 
        GridPuzzleYajikabePlayer
    )(YajikabeSolver)