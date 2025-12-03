from Domain.Puzzles.Meadows.MeadowsSolver import MeadowsSolver
from GridPlayers.GridPuzzle.GridPuzzleMeadowsPlayer import GridPuzzleMeadowsPlayer
from GridProviders.GridPuzzle.GridPuzzleMeadowsGridProvider import GridPuzzleMeadowsGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/meadows", 
        GridPuzzleMeadowsGridProvider, 
        GridPuzzleMeadowsPlayer
    )(MeadowsSolver)