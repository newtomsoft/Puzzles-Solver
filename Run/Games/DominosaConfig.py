from Domain.Puzzles.Dominosa.DominosaSolver import DominosaSolver
from GridPlayers.PuzzlesMobile.PuzzleDominosaPlayer import PuzzleDominosaPlayer
from GridProviders.PuzzlesMobile.PuzzleDominosaGridProvider import PuzzleDominosaGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-dominosa\.com", 
        PuzzleDominosaGridProvider, 
        PuzzleDominosaPlayer
    )(DominosaSolver)