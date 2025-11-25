from Domain.Puzzles.TilePaint.TilePaintSolver import TilePaintSolver
from GridPlayers.GridPuzzle.GridPuzzleTilePaintPlayer import GridPuzzleTilePaintPlayer
from GridProviders.GridPuzzle.GridPuzzleTilePaintGridProvider import GridPuzzleTilePaintGridProvider
from Run.GameRegistry import GameRegistry


def register_tilepaint():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/tilepaint", 
        GridPuzzleTilePaintGridProvider, 
        GridPuzzleTilePaintPlayer
    )(TilePaintSolver)