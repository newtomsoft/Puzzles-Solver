from Domain.Puzzles.Clouds.CloudsSolver import CloudsSolver
from GridPlayers.GridPuzzle.GridPuzzleCloudsPlayer import GridPuzzleCloudsPlayer
from GridProviders.GridPuzzle.GridPuzzleCloudsGridProvider import GridPuzzleCloudsGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/clouds", 
        GridPuzzleCloudsGridProvider, 
        GridPuzzleCloudsPlayer
    )(CloudsSolver)