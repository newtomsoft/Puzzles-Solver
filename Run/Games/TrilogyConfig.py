from Domain.Puzzles.Trilogy.TrilogySolver import TrilogySolver
from GridPlayers.GridPuzzle.GridPuzzleTrilogyPlayer import GridPuzzleTrilogyPlayer
from GridProviders.GridPuzzle.GridPuzzleTrilogyGridProvider import GridPuzzleTrilogyGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/trilogy", 
        GridPuzzleTrilogyGridProvider, 
        GridPuzzleTrilogyPlayer
    )(TrilogySolver)