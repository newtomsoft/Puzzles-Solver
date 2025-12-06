from Domain.Puzzles.Sudoku.Sudoku.SudokuSolver import SudokuSolver
from GridPlayers.GridPuzzle.GridPuzzleSudokuPlayer import GridPuzzleSudokuPlayer
from GridPlayers.PuzzleMobiles.PuzzleSudokuPlayer import PuzzleSudokuPlayer
from GridProviders.EscapeSudoku.EscapeSudokuProvider import EscapeSudokuGridProvider
from GridProviders.GridPuzzle.GridPuzzleSudokuGridProvider import GridPuzzleSudokuGridProvider
from GridProviders.PuzzlesMobile.PuzzleSudokuGridProvider import PuzzleSudokuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-sudoku\.com", 
        PuzzleSudokuGridProvider, 
        PuzzleSudokuPlayer
    )(SudokuSolver)

    GameRegistry.register(
        r"https://escape-sudoku.com/", 
        EscapeSudokuGridProvider, 
        None
    )(SudokuSolver)

    GameRegistry.register(
            r"https://.*gridpuzzle\.com/.*sudoku",
            GridPuzzleSudokuGridProvider,
            GridPuzzleSudokuPlayer
        )(SudokuSolver)

