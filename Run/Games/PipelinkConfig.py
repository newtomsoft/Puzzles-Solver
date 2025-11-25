from Domain.Puzzles.Pipelink.PipelinkSolver import PipelinkSolver
from GridPlayers.GridPuzzle.GridPuzzlePipelinkPlayer import GridPuzzlePipelinkPlayer
from GridProviders.GridPuzzle.GridPuzzlePipelinkGridProvider import GridPuzzlePipelinkGridProvider
from Run.GameRegistry import GameRegistry


def register_pipelink():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/pipelink", 
        GridPuzzlePipelinkGridProvider, 
        GridPuzzlePipelinkPlayer
    )(PipelinkSolver)