from Domain.Puzzles.Akari.AkariSolver import AkariSolver
from GridPlayers.PuzzleBaron.PuzzleBaronLaserGridsGridPlayer import PuzzleBaronLaserGridsPlayer
from GridPlayers.PuzzleMobiles.PuzzleAkariPlayer import PuzzleAkariPlayer
from GridPlayers.Vuqq.VuqqAkariPlayer import VuqqAkariPlayer
from GridProviders.PuzzleBaron.PuzzleBaronLaserGridsGridProvider import PuzzleBaronLaserGridsGridProvider
from GridProviders.PuzzlesMobile.PuzzleAkariGridProvider import PuzzleAkariGridProvider
from GridProviders.Vuqq.VuqqAkariGridProvider import VuqqAkariGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-light-up\.com", 
        PuzzleAkariGridProvider, 
        PuzzleAkariPlayer
    )(AkariSolver)

    GameRegistry.register(
        r"https://lasergrids\.puzzlebaron\.com/init2\.php", 
        PuzzleBaronLaserGridsGridProvider, 
        PuzzleBaronLaserGridsPlayer
    )(AkariSolver)

    GameRegistry.register(
        r"https://vuqq\.com/.*/akari",
        VuqqAkariGridProvider,
        VuqqAkariPlayer
    )(AkariSolver)
