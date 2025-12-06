from Domain.Puzzles.Pipes.PipesSolver import PipesSolver
from GridPlayers.PuzzleMobiles.PuzzlePipesPlayer import PuzzlePipesPlayer
from GridProviders.PuzzlesMobile.PuzzlePipesGridProvider import PuzzlePipesGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-pipes\.com", 
        PuzzlePipesGridProvider, 
        PuzzlePipesPlayer
    )(PipesSolver)