from Domain.Puzzles.Nonogram.NonogramSolver import NonogramSolver
from GridPlayers.PuzzleMobiles.PuzzleNonogramsGrid import PuzzleNonogramsPlayer
from GridProviders.PuzzlesMobile.PuzzleNonogramGridProvider import PuzzleNonogramGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-nonograms\.com", 
        PuzzleNonogramGridProvider, 
        PuzzleNonogramsPlayer
    )(NonogramSolver)