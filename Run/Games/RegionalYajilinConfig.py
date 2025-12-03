from Domain.Puzzles.RegionalYajilin.RegionalYajilinSolver import RegionalYajilinSolver
from GridPlayers.GridPuzzle.GridPuzzleRegionalYajilinPlayer import GridPuzzleRegionalYajilinPlayer
from GridProviders.GridPuzzle.GridPuzzleRegionalYajilinGridProvider import GridPuzzleRegionalYajilinGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/regional-yajilin", 
        GridPuzzleRegionalYajilinGridProvider, 
        GridPuzzleRegionalYajilinPlayer
    )(RegionalYajilinSolver)