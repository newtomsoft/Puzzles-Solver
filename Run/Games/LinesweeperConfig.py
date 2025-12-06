from Domain.Puzzles.Linesweeper.LinesweeperSolver import LinesweeperSolver
from GridPlayers.GridPuzzle.GridPuzzleLinesweeperPlayer import GridPuzzleLinesweeperPlayer
from GridProviders.GridPuzzle.GridPuzzleLinesweeperGridProvider import GridPuzzleLinesweeperGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/linesweeper", 
        GridPuzzleLinesweeperGridProvider, 
        GridPuzzleLinesweeperPlayer
    )(LinesweeperSolver)