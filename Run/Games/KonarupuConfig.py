from Domain.Puzzles.Konarupu.KonarupuSolver import KonarupuSolver
from GridPlayers.GridPuzzle.GridPuzzleKonarupuPlayer import GridPuzzleKonarupuPlayer
from GridProviders.GridPuzzle.GridPuzzleKonarupuGridProvider import GridPuzzleKonarupuGridProvider
from Run.GameRegistry import GameRegistry


def register_konarupu():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/konarupu", 
        GridPuzzleKonarupuGridProvider, 
        GridPuzzleKonarupuPlayer
    )(KonarupuSolver)