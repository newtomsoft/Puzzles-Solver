from Domain.Puzzles.Nonogram.NonogramSolver import NonogramSolver
from GridPlayers.PuzzleMobiles.PuzzleNonogramsGrid import PuzzleNonogramsPlayer
from GridProviders.PuzzlesMobile.PuzzleNonogramsGridProvider import PuzzleNonogramsGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-nonograms\.com", 
        PuzzleNonogramsGridProvider,
        PuzzleNonogramsPlayer
    )(NonogramSolver)