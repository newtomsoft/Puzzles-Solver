from Domain.Puzzles.Akari.AkariSolver import AkariSolver
from GridPlayers.PuzzleBaron.PuzzleBaronLaserGridsGridPlayer import PuzzleBaronLaserGridsPlayer
from GridPlayers.PuzzleMobiles.PuzzleAkariPlayer import PuzzleAkariPlayer
from GridProviders.PuzzleBaron.PuzzleBaronLaserGridsGridProvider import PuzzleBaronLaserGridsGridProvider
from GridProviders.PuzzlesMobile.PuzzleAkariGridProvider import PuzzleAkariGridProvider
from Run.GameRegistry import GameRegistry


def register_akari():
    GameRegistry.register_game(
        r"https://.*\.puzzle-light-up\.com", 
        PuzzleAkariGridProvider, 
        PuzzleAkariPlayer
    )(AkariSolver)

    GameRegistry.register_game(
        r"https://lasergrids\.puzzlebaron\.com/init2\.php", 
        PuzzleBaronLaserGridsGridProvider, 
        PuzzleBaronLaserGridsPlayer
    )(AkariSolver)