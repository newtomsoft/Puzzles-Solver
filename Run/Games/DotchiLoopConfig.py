from Domain.Puzzles.DotchiLoop.DotchiLoopSolver import DotchiLoopSolver
from GridPlayers.GridPuzzle.GridPuzzleDotchiLoopPlayer import GridPuzzleDotchiLoopPlayer
from GridProviders.GridPuzzle.GridPuzzleDotchiLoopGridProvider import GridPuzzleDotchiLoopGridProvider
from Run.GameRegistry import GameRegistry


def register_dotchiloop():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/dotchiloop", 
        GridPuzzleDotchiLoopGridProvider, 
        GridPuzzleDotchiLoopPlayer
    )(DotchiLoopSolver)