from Domain.Puzzles.Skyscrapers.SkyscrapersSolver import SkyscrapersSolver
from GridPlayers.PuzzleMobiles.PuzzleSkyscrapersPlayer import PuzzleSkyScrapersPlayer
from GridProviders.PuzzlesMobile.PuzzleSkyscrapersGridProvider import PuzzleSkyscrapersGridProvider
from Run.GameRegistry import GameRegistry


def register_skyscrapers():
    GameRegistry.register_game(
        r"https://.*\.puzzle-skyscrapers\.com", 
        PuzzleSkyscrapersGridProvider, 
        PuzzleSkyScrapersPlayer
    )(SkyscrapersSolver)