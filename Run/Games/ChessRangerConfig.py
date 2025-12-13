from Domain.Puzzles.ChessRanger.ChessRangerSolver import ChessRangerSolver
from GridPlayers.PuzzleMobiles.PuzzleChessRangerPlayer import PuzzleChessRangerPlayer
from GridProviders.PuzzlesMobile.PuzzleChessRangerGridProvider import PuzzleChessRangerGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-chess\.com",
        PuzzleChessRangerGridProvider,
        PuzzleChessRangerPlayer
    )(ChessRangerSolver)
