from Domain.Puzzles.Koburin.KoburinSolver import KoburinSolver
from GridPlayers.GridPuzzle.GridPuzzleKoburinPlayer import GridPuzzleKoburinPlayer
from GridProviders.GridPuzzle.GridPuzzleKoburinGridProvider import GridPuzzleKoburinGridProvider
from Run.GameRegistry import GameRegistry


def register_koburin():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/koburin", 
        GridPuzzleKoburinGridProvider, 
        GridPuzzleKoburinPlayer
    )(KoburinSolver)