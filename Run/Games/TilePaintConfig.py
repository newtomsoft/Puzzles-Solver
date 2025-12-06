from Domain.Puzzles.TilePaint.TilePaintSolver import TilePaintSolver
from GridPlayers.GridPuzzle.GridPuzzleTilePaintPlayer import GridPuzzleTilePaintPlayer
from GridProviders.GridPuzzle.GridPuzzleTilePaintGridProvider import GridPuzzleTilePaintGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/tilepaint", 
        GridPuzzleTilePaintGridProvider, 
        GridPuzzleTilePaintPlayer
    )(TilePaintSolver)