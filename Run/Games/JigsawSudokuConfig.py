from Domain.Puzzles.Sudoku.JigsawSudoku.JigsawSudokuSolver import JigsawSudokuSolver
from GridPlayers.PuzzleMobiles.PuzzleSudokuPlayer import PuzzleSudokuPlayer
from GridProviders.PuzzlesMobile.PuzzleJigsawSudokuGridProvider import PuzzleJigsawSudokuGridProvider
from Run.GameRegistry import GameRegistry


def register_jigsawsudoku():
    GameRegistry.register_game(
        r"https://.*\.puzzle-jigsaw-sudoku\.com", 
        PuzzleJigsawSudokuGridProvider, 
        PuzzleSudokuPlayer
    )(JigsawSudokuSolver)