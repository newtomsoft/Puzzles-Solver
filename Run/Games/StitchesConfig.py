from Domain.Puzzles.Stitches.StitchesSolver import StitchesSolver
from GridPlayers.PuzzleMobiles.PuzzleStitchesPlayer import PuzzleStitchesPlayer
from GridProviders.PuzzlesMobile.PuzzleStitchesGridProvider import PuzzleStitchesGridProvider
from Run.GameRegistry import GameRegistry


def register_stitches():
    GameRegistry.register_game(
        r"https://.*\.puzzle-stitches\.com", 
        PuzzleStitchesGridProvider, 
        PuzzleStitchesPlayer
    )(StitchesSolver)