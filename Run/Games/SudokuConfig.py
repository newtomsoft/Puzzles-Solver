from Domain.Puzzles.Sudoku.Sudoku.SudokuSolver import SudokuSolver
from GridPlayers.PuzzleMobiles.PuzzleSudokuPlayer import PuzzleSudokuPlayer
from GridPlayers.GridPuzzle.GridPuzzleSudokuPlayer import GridPuzzleSudokuPlayer
from GridProviders.EscapeSudoku.EscapeSudokuProvider import EscapeSudokuGridProvider
from GridProviders.GridPuzzle.GridPuzzleSudokuGridProvider import GridPuzzleSudokuGridProvider
from GridProviders.PuzzlesMobile.PuzzleSudokuGridProvider import PuzzleSudokuGridProvider
from Run.GameRegistry import GameRegistry


def register_sudoku():
    GameRegistry.register_game(
        r"https://.*\.puzzle-sudoku\.com", 
        PuzzleSudokuGridProvider, 
        PuzzleSudokuPlayer
    )(SudokuSolver)

    GameRegistry.register_game(
        r"https://escape-sudoku.com/", 
        EscapeSudokuGridProvider, 
        None
    )(SudokuSolver)

    GameRegistry.register_game(
            r"https://.*gridpuzzle\.com/.*sudoku",
            GridPuzzleSudokuGridProvider,
            GridPuzzleSudokuPlayer
        )(SudokuSolver)

