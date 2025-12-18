from Domain.Puzzles.MinesweeperMosaic.MinesweeperMosaicSolver import MinesweeperMosaicSolver
from GridPlayers.PuzzleMobiles.PuzzleMinesweeperMosaicPlayer import PuzzleMinesweeperMosaicPlayer
from GridProviders.PuzzlesMobile.PuzzleMinesweeperMosaicGridProvider import PuzzleMinesweeperMosaicGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://(?:.*\.)?puzzle-minesweeper\.com/.*mosaic",
        PuzzleMinesweeperMosaicGridProvider,
        PuzzleMinesweeperMosaicPlayer
    )(MinesweeperMosaicSolver)
