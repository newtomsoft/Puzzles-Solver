from Domain.Puzzles.Norinori.NorinoriSolver import NorinoriSolver
from GridPlayers.GridPuzzle.GridPuzzleNorinoriPlayer import GridPuzzleNorinoriPlayer
from GridPlayers.PuzzlesMobile.PuzzleNorinoriPlayer import PuzzleNorinoriPlayer
from GridProviders.GridPuzzle.GridPuzzleNorinoriGridProvider import GridPuzzleNorinoriGridProvider
from GridProviders.PuzzlesMobile.PuzzleNorinoriGridProvider import PuzzleNorinoriGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-norinori\.com", 
        PuzzleNorinoriGridProvider, 
        PuzzleNorinoriPlayer
    )(NorinoriSolver)

    (GameRegistry.register(
        r"https://.*gridpuzzle\.com/norinori",
        GridPuzzleNorinoriGridProvider,
        GridPuzzleNorinoriPlayer
    )(NorinoriSolver))