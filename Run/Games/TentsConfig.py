from Domain.Puzzles.Tents.TentsSolver import TentsSolver
from GridPlayers.PuzzleBaron.PuzzleBaronCampsitesGridPlayer import PuzzleBaronCampsitesPlayer
from GridPlayers.PuzzleMobiles.PuzzleTentsPlayer import PuzzleTentsPlayer
from GridProviders.PuzzleBaron.PuzzleBaronCampsitesGridProvider import PuzzleBaronCampsitesGridProvider
from GridProviders.PuzzlesMobile.PuzzleTentsGridProvider import PuzzleTentsGridProvider
from GridProviders.Vuqq.VuqqTentsAndTreesGridProvider import VuqqTentsAndTreesGridProvider
from GridPlayers.Vuqq.VuqqTentsAndTreesPlayer import VuqqTentsAndTreesPlayer
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-tents\.com", 
        PuzzleTentsGridProvider, 
        PuzzleTentsPlayer
    )(TentsSolver)
    
    GameRegistry.register(
        r"https://vuqq\.com/.*tents.*",
        VuqqTentsAndTreesGridProvider,
        VuqqTentsAndTreesPlayer
    )(TentsSolver)

    GameRegistry.register(
        r"https://campsites\.puzzlebaron\.com/init2\.php", 
        PuzzleBaronCampsitesGridProvider, 
        PuzzleBaronCampsitesPlayer
    )(TentsSolver)