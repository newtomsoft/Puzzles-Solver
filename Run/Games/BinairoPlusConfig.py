from Domain.Puzzles.BinairoPlus.BinairoPlusSolver import BinairoPlusSolver
from GridPlayers.LinkedIn.TangoPlayer import TangoPlayer
from GridPlayers.PuzzleMobiles.PuzzleBinairoPlayer import PuzzleBinairoPlayer
from GridProviders.Linkedin.TangoGridProvider import TangoGridProvider
from GridProviders.PuzzlesMobile.PuzzleBinairoPlusGridProvider import PuzzleBinairoPlusGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://www\.linkedin\.com/games/tango", 
        TangoGridProvider, 
        TangoPlayer
    )(BinairoPlusSolver)

    GameRegistry.register(
        r"https://.*\.puzzle-binairo\.com/.*binairo-plus", 
        PuzzleBinairoPlusGridProvider, 
        PuzzleBinairoPlayer
    )(BinairoPlusSolver)