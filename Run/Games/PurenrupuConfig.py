from Domain.Puzzles.Purenrupu.PurenrupuSolver import PurenrupuSolver
from GridPlayers.GridPuzzle.GridPuzzlePurenrupuPlayer import GridPuzzlePurenrupuPlayer
from GridProviders.GridPuzzle.GridPuzzlePurenrupuGridProvider import GridPuzzlePurenrupuGridProvider
from Run.GameRegistry import GameRegistry


def register_purenrupu():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/pure-loop", 
        GridPuzzlePurenrupuGridProvider, 
        GridPuzzlePurenrupuPlayer
    )(PurenrupuSolver)