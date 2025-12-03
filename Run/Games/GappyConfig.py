from Domain.Puzzles.Gappy.GappySolver import GappySolver
from GridPlayers.GridPuzzle.GridPuzzleGappyPlayer import GridPuzzleGappyPlayer
from GridProviders.GridPuzzle.GridPuzzleGappyGridProvider import GridPuzzleGappyGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/gappy", 
        GridPuzzleGappyGridProvider, 
        GridPuzzleGappyPlayer
    )(GappySolver)