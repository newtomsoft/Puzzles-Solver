from Domain.Puzzles.TentaiShow.TentaiShowSolver import TentaiShowSolver
from GridPlayers.GridPuzzle.GridPuzzleGalaxiesPlayer import GridPuzzleGalaxiesPlayer
from GridPlayers.PuzzleMobiles.PuzzleGalaxiesPlayer import PuzzleGalaxiesPlayer
from GridProviders.GridPuzzle.GridPuzzleGalaxiesGridProvider import GridPuzzleGalaxiesGridProvider
from GridProviders.PuzzlesMobile.PuzzleGalaxiesGridProvider import PuzzleGalaxiesGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-galaxies\.com", 
        PuzzleGalaxiesGridProvider, 
        PuzzleGalaxiesPlayer
    )(TentaiShowSolver)

    GameRegistry.register(
        r"https://.*gridpuzzle\.com/galaxies", 
        GridPuzzleGalaxiesGridProvider, 
        GridPuzzleGalaxiesPlayer
    )(TentaiShowSolver)