from Domain.Puzzles.Stitches.StitchesSolver import StitchesSolver
from GridPlayers.PuzzlesMobile.PuzzleStitchesPlayer import PuzzleStitchesPlayer
from GridProviders.PuzzlesMobile.PuzzleStitchesGridProvider import PuzzleStitchesGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-stitches\.com", 
        PuzzleStitchesGridProvider, 
        PuzzleStitchesPlayer
    )(StitchesSolver)