from Domain.Puzzles.NumberLink.NumberLinkSolver import NumberLinkSolver
from Domain.Puzzles.ArukoneNo2x2.ArukoneNo2x2Solver import ArukoneNo2x2Solver
from GridPlayers.GridPuzzle.GridPuzzleArukoneNo2x2Player import GridPuzzleArukoneNo2x2Player
from GridPlayers.GridPuzzle.GridPuzzleArukonePlayer import GridPuzzleArukonePlayer
from GridPlayers.PuzzleBaron.PuzzleBaronNumberLinksGridPlayer import PuzzleBaronNumberLinksPlayer
from GridProviders.GridPuzzle.GridPuzzleArukoneNo2x2GridProvider import GridPuzzleArukoneNo2x2GridProvider
from GridProviders.GridPuzzle.GridPuzzleArukoneGridProvider import GridPuzzleArukoneGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronNumberLinksGridProvider import PuzzleBaronNumberLinksGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://numberlinks\.puzzlebaron\.com/init2\.php",
        PuzzleBaronNumberLinksGridProvider,
        PuzzleBaronNumberLinksPlayer
    )(NumberLinkSolver)

    GameRegistry.register(
        r"https://gridpuzzle\.com/arukone-no-2x2",
        GridPuzzleArukoneNo2x2GridProvider,
        GridPuzzleArukoneNo2x2Player
    )(ArukoneNo2x2Solver)

    GameRegistry.register(
        r"https://gridpuzzle\.com/arukone($|/)",
        GridPuzzleArukoneGridProvider,
        GridPuzzleArukonePlayer
    )(NumberLinkSolver)