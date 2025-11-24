from Domain.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver
from GridPlayers.GridPuzzle.GridPuzzleMinesweeperPlayer import GridPuzzleMinesweeperPlayer
from GridPlayers.PuzzleMobiles.PuzzleMinesweeperPlayer import PuzzleMinesweeperPlayer
from GridProviders.GridPuzzle.GridPuzzleMinesweeperGridProvider import GridPuzzleMinesweeperGridProvider
from GridProviders.PuzzlesMobile.PuzzleMinesweeperMosaicGridProvider import PuzzleMinesweeperMosaicGridProvider
from Run.GameRegistry import GameRegistry


def register_minesweeper():
    GameRegistry.register_game(
        r"https://.*\.puzzle-minesweeper\.com", 
        PuzzleMinesweeperMosaicGridProvider, 
        PuzzleMinesweeperPlayer
    )(MinesweeperSolver)

    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/minesweeper", 
        GridPuzzleMinesweeperGridProvider, 
        GridPuzzleMinesweeperPlayer
    )(MinesweeperSolver)