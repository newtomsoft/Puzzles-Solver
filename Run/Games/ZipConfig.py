from Domain.Puzzles.Zip.ZipSolver import ZipSolver
from GridPlayers.LinkedIn.ZipPlayer import ZipPlayer
from GridProviders.Linkedin.ZipGridProvider import ZipGridProvider
from Run.GameRegistry import GameRegistry


def register_zip():
    GameRegistry.register_game(
        r"https://www\.linkedin\.com/games/zip", 
        ZipGridProvider, 
        ZipPlayer
    )(ZipSolver)