from PuzzleSolver.Puzzles.Yakazu.YakazuSolver import YakazuSolver
from GridPlayers.GridPuzzle.GridPuzzleYakuzuPlayer import GridPuzzleYakazuPlayer
from GridProviders.GridPuzzle.GridPuzzleYakuzuGridProvider import GridPuzzleYakazuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/yakazu", 
        GridPuzzleYakazuGridProvider, 
        GridPuzzleYakazuPlayer
    )(YakazuSolver)
