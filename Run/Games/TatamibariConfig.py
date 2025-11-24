from Domain.Puzzles.Tatamibari.TatamibariSolver import TatamibariSolver
from GridPlayers.GridPuzzle.GridPuzzleTatamibariPlayer import GridPuzzleTatamibariPlayer
from GridProviders.GridPuzzle.GridPuzzleTatamibariGridProvider import GridPuzzleTatamibariGridProvider
from Run.GameRegistry import GameRegistry


def register_tatamibari():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/tatamibari", 
        GridPuzzleTatamibariGridProvider, 
        GridPuzzleTatamibariPlayer
    )(TatamibariSolver)