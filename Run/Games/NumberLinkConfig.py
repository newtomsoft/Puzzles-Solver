from Domain.Puzzles.NumberLink.NumberLinkSolver import NumberLinkSolver
from GridPlayers.PuzzleBaron.PuzzleBaronNumberLinksGridPlayer import PuzzleBaronNumberLinksPlayer
from GridProviders.PuzzleBaron.PuzzleBaronNumberLinksGridProvider import PuzzleBaronNumberLinksGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://numberlinks\.puzzlebaron\.com/init2\.php", 
        PuzzleBaronNumberLinksGridProvider, 
        PuzzleBaronNumberLinksPlayer
    )(NumberLinkSolver)