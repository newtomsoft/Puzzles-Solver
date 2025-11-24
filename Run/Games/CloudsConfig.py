from Domain.Puzzles.Clouds.CloudsSolver import CloudsSolver
from GridPlayers.GridPuzzle.GridPuzzleCloudsPlayer import GridPuzzleCloudsPlayer
from GridProviders.GridPuzzle.GridPuzzleCloudsGridProvider import GridPuzzleCloudsGridProvider
from Run.GameRegistry import GameRegistry


def register_clouds():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/clouds", 
        GridPuzzleCloudsGridProvider, 
        GridPuzzleCloudsPlayer
    )(CloudsSolver)