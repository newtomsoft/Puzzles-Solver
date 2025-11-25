from Domain.Puzzles.Dominosa.DominosaSolver import DominosaSolver
from GridPlayers.PuzzleMobiles.PuzzleDominosaPlayer import PuzzleDominosaPlayer
from GridProviders.PuzzlesMobile.PuzzleDominosaGridProvider import PuzzleDominosaGridProvider
from Run.GameRegistry import GameRegistry


def register_dominosa():
    GameRegistry.register_game(
        r"https://.*\.puzzle-dominosa\.com", 
        PuzzleDominosaGridProvider, 
        PuzzleDominosaPlayer
    )(DominosaSolver)