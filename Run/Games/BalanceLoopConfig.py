from Domain.Puzzles.BalanceLoop.BalanceLoopSolver import BalanceLoopSolver
from GridPlayers.GridPuzzle.GridPuzzleBalanceLoopPlayer import GridPuzzleBalanceLoopPlayer
from GridProviders.GridPuzzle.GridPuzzleBalanceLoopGridProvider import GridPuzzleBalanceLoopGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/balance-loop", 
        GridPuzzleBalanceLoopGridProvider, 
        GridPuzzleBalanceLoopPlayer
    )(BalanceLoopSolver)