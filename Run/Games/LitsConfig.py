from Domain.Puzzles.Lits.LitsSolver import LitsSolver
from GridPlayers.PuzzleMobiles.PuzzleLitsPlayer import PuzzleLitsPlayer
from GridProviders.PuzzlesMobile.PuzzleLitsGridProvider import PuzzleLitsGridProvider
from Run.GameRegistry import GameRegistry


def register_lits():
    GameRegistry.register_game(
        r"https://.*\.puzzle-lits\.com", 
        PuzzleLitsGridProvider, 
        PuzzleLitsPlayer
    )(LitsSolver)