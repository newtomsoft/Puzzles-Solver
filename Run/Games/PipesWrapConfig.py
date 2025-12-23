from Domain.Puzzles.PipesWrap.PipesWrapSolver import PipesWrapSolver
from GridPlayers.PuzzlesMobile.PuzzlePipesPlayer import PuzzlePipesPlayer
from GridProviders.PuzzlesMobile.PuzzlePipesGridProvider import PuzzlePipesGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-pipes\.com/\?size=\\d{2,}", 
        PuzzlePipesGridProvider, 
        PuzzlePipesPlayer
    )(PipesWrapSolver)