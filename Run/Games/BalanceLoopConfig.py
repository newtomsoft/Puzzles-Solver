from Domain.Puzzles.BalanceLoop.BalanceLoopSolver import BalanceLoopSolver
from GridPlayers.GridPuzzle.GridPuzzleBalanceLoopPlayer import GridPuzzleBalanceLoopPlayer
from GridProviders.GridPuzzle.GridPuzzleBalanceLoopGridProvider import GridPuzzleBalanceLoopGridProvider
from Run.GameRegistry import GameRegistry


def register_balanceloop():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/balance-loop", 
        GridPuzzleBalanceLoopGridProvider, 
        GridPuzzleBalanceLoopPlayer
    )(BalanceLoopSolver)