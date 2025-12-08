from Domain.Puzzles.Kuroshiro.KuroshiroSolver import KuroshiroSolver
from GridPlayers.GridPuzzle.GridPuzzleShirokuroPlayer import GridPuzzleShirokuroPlayer
from GridProviders.GridPuzzle.GridPuzzleShirokuroGridProvider import GridPuzzleShirokuroGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/shirokuro", 
        GridPuzzleShirokuroGridProvider, 
        GridPuzzleShirokuroPlayer
    )(KuroshiroSolver)
