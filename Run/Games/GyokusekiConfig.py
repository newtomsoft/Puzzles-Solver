from Domain.Puzzles.Gyokuseki.GyokusekiSolver import GyokusekiSolver
from GridPlayers.GridPuzzle.GridPuzzleGyokusekiPlayer import GridPuzzleGyokusekiPlayer
from GridProviders.GridPuzzle.GridPuzzleGyokusekiGridProvider import GridPuzzleGyokusekiGridProvider
from Run.GameRegistry import GameRegistry


def register_gyokuseki():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/gyokuseki", 
        GridPuzzleGyokusekiGridProvider, 
        GridPuzzleGyokusekiPlayer
    )(GyokusekiSolver)