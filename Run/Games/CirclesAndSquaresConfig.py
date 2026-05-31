from PuzzleSolver.Puzzles.CirclesAndSquares.CirclesAndSquaresSolver import CirclesAndSquaresSolver
from GridPlayers.GridPuzzle.GridPuzzleCirclesAndSquaresPlayer import GridPuzzleCirclesAndSquaresPlayer
from GridProviders.GridPuzzle.GridPuzzleCirclesAndSquaresGridProvider import GridPuzzleCirclesAndSquaresGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/circles-and-squares", 
        GridPuzzleCirclesAndSquaresGridProvider, 
        GridPuzzleCirclesAndSquaresPlayer
    )(CirclesAndSquaresSolver)