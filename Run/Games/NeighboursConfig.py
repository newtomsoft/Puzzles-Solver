from Domain.Puzzles.Neighbours.NeighboursSolver import NeighboursSolver
from GridPlayers.GridPuzzle.GridPuzzleNeighboursPlayer import GridPuzzleNeighboursPlayer
from GridProviders.GridPuzzle.GridPuzzleNeighboursGridProvider import GridPuzzleNeighboursGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/neighbours", 
        GridPuzzleNeighboursGridProvider, 
        GridPuzzleNeighboursPlayer
    )(NeighboursSolver)