from Domain.Puzzles.Sudoku.KillerSudoku.KillerSudokuSolver import KillerSudokuSolver
from GridPlayers.PuzzleMobiles.PuzzleSudokuPlayer import PuzzleSudokuPlayer
from GridProviders.PuzzlesMobile.PuzzleKillerSudokuGridProvider import PuzzleKillerSudokuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-killer-sudoku\.com", 
        PuzzleKillerSudokuGridProvider, 
        PuzzleSudokuPlayer
    )(KillerSudokuSolver)