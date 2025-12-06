from Domain.Puzzles.Yajilin.YajilinSolver import YajilinSolver
from GridPlayers.GridPuzzle.GridPuzzleYajilinPlayer import GridPuzzleYajilinPlayer
from GridProviders.GridPuzzle.GridPuzzleYajilinGridProvider import GridPuzzleYajilinGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/yajilin", 
        GridPuzzleYajilinGridProvider, 
        GridPuzzleYajilinPlayer
    )(YajilinSolver)