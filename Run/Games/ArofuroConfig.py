from Domain.Puzzles.Arofuro.ArofuroSolver import ArofuroSolver
from GridPlayers.GridPuzzle.GridPuzzleArofuroPlayer import GridPuzzleArofuroPlayer
from GridProviders.GridPuzzle.GridPuzzleArofuroGridProvider import GridPuzzleArofuroGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/arofuro", 
        GridPuzzleArofuroGridProvider, 
        GridPuzzleArofuroPlayer
    )(ArofuroSolver)
