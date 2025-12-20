from Domain.Puzzles.Skyscrapers.SkyscrapersSolver import SkyscrapersSolver
from GridPlayers.PuzzleMobiles.PuzzleSkyscrapersPlayer import PuzzleSkyScrapersPlayer
from GridPlayers.Vuqq.VuqqSkyscrapersPlayer import VuqqSkyscrapersPlayer
from GridProviders.PuzzlesMobile.PuzzleSkyscrapersGridProvider import PuzzleSkyscrapersGridProvider
from GridProviders.Vuqq.VuqqSkyscrapersGridProvider import VuqqSkyscrapersGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-skyscrapers\.com",
        PuzzleSkyscrapersGridProvider,
        PuzzleSkyScrapersPlayer
    )(SkyscrapersSolver)

    GameRegistry.register(
        r"https://vuqq\.com/.*skyscrapers/", 
        VuqqSkyscrapersGridProvider, 
        VuqqSkyscrapersPlayer
    )(SkyscrapersSolver)