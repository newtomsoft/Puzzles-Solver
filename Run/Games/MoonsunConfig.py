from Domain.Puzzles.Moonsun.MoonsunSolver import MoonsunSolver
from GridPlayers.GridPuzzle.GridPuzzleMoonsunPlayer import GridPuzzleMoonsunPlayer
from GridProviders.GridPuzzle.GridPuzzleMoonsunGridProvider import GridPuzzleMoonsunGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/moonsun", 
        GridPuzzleMoonsunGridProvider, 
        GridPuzzleMoonsunPlayer
    )(MoonsunSolver)