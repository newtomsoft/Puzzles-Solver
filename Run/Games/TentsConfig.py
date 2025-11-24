from Domain.Puzzles.Tents.TentsSolver import TentsSolver
from GridPlayers.PuzzleBaron.PuzzleBaronCampsitesGridPlayer import PuzzleBaronCampsitesPlayer
from GridPlayers.PuzzleMobiles.PuzzleTentsPlayer import PuzzleTentsPlayer
from GridProviders.PuzzleBaron.PuzzleBaronCampsitesGridProvider import PuzzleBaronCampsitesGridProvider
from GridProviders.PuzzlesMobile.PuzzleTentsGridProvider import PuzzleTentsGridProvider
from Run.GameRegistry import GameRegistry


def register_tents():
    GameRegistry.register_game(
        r"https://.*\.puzzle-tents\.com", 
        PuzzleTentsGridProvider, 
        PuzzleTentsPlayer
    )(TentsSolver)

    GameRegistry.register_game(
        r"https://campsites\.puzzlebaron\.com/init2\.php", 
        PuzzleBaronCampsitesGridProvider, 
        PuzzleBaronCampsitesPlayer
    )(TentsSolver)