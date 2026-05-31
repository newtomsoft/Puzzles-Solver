from PuzzleSolver.Puzzles.KenKen.KenKenSolver import KenKenSolver
from GridPlayers.GridPuzzle.GridPuzzleKenKenPlayer import GridPuzzleKenKenPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronCalcudokuGridPlayer import PuzzleBaronCalcudokuPlayer
from GridProviders.GridPuzzle.GridPuzzleKenKenGridProvider import GridPuzzleKenKenGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronCalcudokuGridProvider import PuzzleBaronCalcudokuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://calcudoku\.puzzlebaron\.com/init2\.php", 
        PuzzleBaronCalcudokuGridProvider, 
        PuzzleBaronCalcudokuPlayer
    )(KenKenSolver)

    GameRegistry.register(
        r"https://(www\.)?gridpuzzles?\.com/calcudoku",
        GridPuzzleKenKenGridProvider,
        GridPuzzleKenKenPlayer
    )(KenKenSolver)