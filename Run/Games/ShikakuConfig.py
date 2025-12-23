from Domain.Puzzles.Shikaku.ShikakuSolver import ShikakuSolver
from GridPlayers.PuzzlesMobile.PuzzleShikakuPlayer import PuzzleShikakuPlayer
from GridProviders.PuzzlesMobile.PuzzleShikakuGridProvider import PuzzleShikakuGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-shikaku\.com", 
        PuzzleShikakuGridProvider, 
        PuzzleShikakuPlayer
    )(ShikakuSolver)