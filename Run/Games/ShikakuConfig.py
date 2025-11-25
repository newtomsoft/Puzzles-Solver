from Domain.Puzzles.Shikaku.ShikakuSolver import ShikakuSolver
from GridPlayers.PuzzleMobiles.PuzzleShikakuPlayer import PuzzleShikakuPlayer
from GridProviders.PuzzlesMobile.PuzzleShikakuGridProvider import PuzzleShikakuGridProvider
from Run.GameRegistry import GameRegistry


def register_shikaku():
    GameRegistry.register_game(
        r"https://.*\.puzzle-shikaku\.com", 
        PuzzleShikakuGridProvider, 
        PuzzleShikakuPlayer
    )(ShikakuSolver)