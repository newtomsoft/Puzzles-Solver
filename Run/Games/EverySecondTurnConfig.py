from Domain.Puzzles.EverySecondTurn.EverySecondTurnSolver import EverySecondTurnSolver
from GridPlayers.GridPuzzle.GridPuzzleEverySecondTurnPlayer import GridPuzzleEverySecondTurnPlayer
from GridProviders.GridPuzzle.GridPuzzleEverySecondTurnGridProvider import GridPuzzleEverySecondTurnGridProvider
from Run.GameRegistry import GameRegistry


def register_everysecondturn():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/every-second-turn", 
        GridPuzzleEverySecondTurnGridProvider, 
        GridPuzzleEverySecondTurnPlayer
    )(EverySecondTurnSolver)