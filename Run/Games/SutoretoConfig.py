from Domain.Puzzles.Sutoreto.SutoretoSolver import SutoretoSolver
from GridPlayers.GridPuzzle.GridPuzzleSutoretoPlayer import GridPuzzleSutoretoPlayer
from GridProviders.GridPuzzle.GridPuzzleSutoretoGridProvider import GridPuzzleSutoretoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/sutoreto", 
        GridPuzzleSutoretoGridProvider, 
        GridPuzzleSutoretoPlayer
    )(SutoretoSolver)
