from Domain.Puzzles.Pipes.PipesSolver import PipesSolver
from GridPlayers.PuzzleMobiles.PuzzlePipesPlayer import PuzzlePipesPlayer
from GridPlayers.Vuqq.VuqqNetwalkPlayer import VuqqNetwalkPlayer
from GridProviders.PuzzlesMobile.PuzzlePipesGridProvider import PuzzlePipesGridProvider
from GridProviders.Vuqq.VuqqNetwalkGridProvider import VuqqNetwalkGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-pipes\.com", 
        PuzzlePipesGridProvider, 
        PuzzlePipesPlayer
    )(PipesSolver)

    GameRegistry.register(
        r"https://vuqq\.com/.*/netwalk/.*",
        VuqqNetwalkGridProvider,
        VuqqNetwalkPlayer
    )(PipesSolver)