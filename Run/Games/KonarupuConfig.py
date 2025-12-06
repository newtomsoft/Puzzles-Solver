from Domain.Puzzles.Konarupu.KonarupuSolver import KonarupuSolver
from GridPlayers.GridPuzzle.GridPuzzleKonarupuPlayer import GridPuzzleKonarupuPlayer
from GridProviders.GridPuzzle.GridPuzzleKonarupuGridProvider import GridPuzzleKonarupuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/konarupu", 
        GridPuzzleKonarupuGridProvider, 
        GridPuzzleKonarupuPlayer
    )(KonarupuSolver)