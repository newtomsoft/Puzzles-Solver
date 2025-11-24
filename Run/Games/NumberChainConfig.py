from Domain.Puzzles.NumberChain.NumberChainSolver import NumberChainSolver
from GridPlayers.GridPuzzle.GridPuzzleNumberChainPlayer import GridPuzzleNumberChainPlayer
from GridProviders.GridPuzzle.GridPuzzleNumberChainGridProvider import GridPuzzleNumberChainGridProvider
from Run.GameRegistry import GameRegistry


def register_numberchain():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/number-chain", 
        GridPuzzleNumberChainGridProvider, 
        GridPuzzleNumberChainPlayer
    )(NumberChainSolver)