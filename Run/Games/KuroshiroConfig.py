from Domain.Puzzles.Kuroshiro.KuroshiroSolver import KuroshiroSolver
from GridPlayers.GridPuzzle.GridPuzzleKuroshiroPlayer import GridPuzzleKuroshiroPlayer
from GridProviders.GridPuzzle.GridPuzzleKuroshiroGridProvider import GridPuzzleKuroshiroGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/kuroshiro", 
        GridPuzzleKuroshiroGridProvider, 
        GridPuzzleKuroshiroPlayer
    )(KuroshiroSolver)