from Domain.Puzzles.KenKen.KenKenSolver import KenKenSolver
from GridPlayers.PuzzleBaron.PuzzleBaronCalcudokuGridPlayer import PuzzleBaronCalcudokuPlayer
from GridProviders.PuzzleBaron.PuzzleBaronCalcudokuGridProvider import PuzzleBaronCalcudokuGridProvider
from Run.GameRegistry import GameRegistry


def register_kenken():
    GameRegistry.register_game(
        r"https://calcudoku\.puzzlebaron\.com/init2\.php", 
        PuzzleBaronCalcudokuGridProvider, 
        PuzzleBaronCalcudokuPlayer
    )(KenKenSolver)