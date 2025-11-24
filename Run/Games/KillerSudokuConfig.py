from Domain.Puzzles.Sudoku.KillerSudoku.KillerSudokuSolver import KillerSudokuSolver
from GridPlayers.PuzzleMobiles.PuzzleSudokuPlayer import PuzzleSudokuPlayer
from GridProviders.PuzzlesMobile.PuzzleKillerSudokuGridProvider import PuzzleKillerSudokuGridProvider
from Run.GameRegistry import GameRegistry


def register_killersudoku():
    GameRegistry.register_game(
        r"https://.*\.puzzle-killer-sudoku\.com", 
        PuzzleKillerSudokuGridProvider, 
        PuzzleSudokuPlayer
    )(KillerSudokuSolver)