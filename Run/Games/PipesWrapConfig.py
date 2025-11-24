from Domain.Puzzles.PipesWrap.PipesWrapSolver import PipesWrapSolver
from GridPlayers.PuzzleMobiles.PuzzlePipesPlayer import PuzzlePipesPlayer
from GridProviders.PuzzlesMobile.PuzzlePipesGridProvider import PuzzlePipesGridProvider
from Run.GameRegistry import GameRegistry


def register_pipeswrap():
    GameRegistry.register_game(
        r"https://.*\.puzzle-pipes\.com/\?size=\\d{2,}", 
        PuzzlePipesGridProvider, 
        PuzzlePipesPlayer
    )(PipesWrapSolver)