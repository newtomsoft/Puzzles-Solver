from PuzzleSolver.Puzzles.Herugolf.HerugolfSolver import HerugolfSolver
from GridPlayers.PuzzLink.PuzzLinkHerugolfPlayer import PuzzLinkHerugolfPlayer
from GridProviders.PuzzLink.PuzzLinkHerugolfGridProvider import PuzzLinkHerugolfGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*puzz\.link/.*herugolf",
        PuzzLinkHerugolfGridProvider,
        PuzzLinkHerugolfPlayer,
    )(HerugolfSolver)
