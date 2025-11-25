from Domain.Puzzles.Neighbours.NeighboursSolver import NeighboursSolver
from GridPlayers.GridPuzzle.GridPuzzleNeighboursPlayer import GridPuzzleNeighboursPlayer
from GridProviders.GridPuzzle.GridPuzzleNeighboursGridProvider import GridPuzzleNeighboursGridProvider
from Run.GameRegistry import GameRegistry


def register_neighbours():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/neighbours", 
        GridPuzzleNeighboursGridProvider, 
        GridPuzzleNeighboursPlayer
    )(NeighboursSolver)