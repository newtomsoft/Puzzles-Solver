from Domain.Puzzles.GrandTour.GrandTourSolver import GrandTourSolver
from GridPlayers.GridPuzzle.GridPuzzleGrandTourPlayer import GridPuzzleGrandTourPlayer
from GridProviders.GridPuzzle.GridPuzzleGrandTourGridProvider import GridPuzzleGrandTourGridProvider
from Run.GameRegistry import GameRegistry


def register_grandtour():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/grandtour", 
        GridPuzzleGrandTourGridProvider, 
        GridPuzzleGrandTourPlayer
    )(GrandTourSolver)