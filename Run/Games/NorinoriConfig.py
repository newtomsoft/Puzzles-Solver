from Domain.Puzzles.Norinori.NorinoriSolver import NorinoriSolver
from GridPlayers.PuzzleMobiles.PuzzleNorinoriPlayer import PuzzleNorinoriPlayer
from GridProviders.PuzzlesMobile.PuzzleNorinoriGridProvider import PuzzleNorinoriGridProvider
from Run.GameRegistry import GameRegistry


def register_norinori():
    GameRegistry.register_game(
        r"https://.*\.puzzle-norinori\.com", 
        PuzzleNorinoriGridProvider, 
        PuzzleNorinoriPlayer
    )(NorinoriSolver)