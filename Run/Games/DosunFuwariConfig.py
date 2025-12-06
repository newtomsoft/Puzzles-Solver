from Domain.Puzzles.DosunFuwari.DosunFuwariSolver import DosunFuwariSolver
from GridPlayers.GridPuzzle.GridPuzzleDosunFuwariPlayer import GridPuzzleDosunFuwariPlayer
from GridProviders.GridPuzzle.GridPuzzleDosunFuwariGridProvider import GridPuzzleDosunFuwariGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/dosun-fuwari", 
        GridPuzzleDosunFuwariGridProvider, 
        GridPuzzleDosunFuwariPlayer
    )(DosunFuwariSolver)