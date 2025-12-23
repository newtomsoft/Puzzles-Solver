from Domain.Puzzles.Kurodoko.KurodokoSolver import KurodokoSolver
from GridPlayers.PuzzlesMobile.PuzzleKurodokoPlayer import PuzzleKurodokoPlayer
from GridProviders.PuzzlesMobile.PuzzleKurodokoGridProvider import PuzzleKurodokoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-kurodoko\.com",
        PuzzleKurodokoGridProvider,
        PuzzleKurodokoPlayer
    )(KurodokoSolver)

    GameRegistry.register(
        r"https://.*\.puzzles-mobile\.com/kurodoko",
        PuzzleKurodokoGridProvider,
        PuzzleKurodokoPlayer
    )(KurodokoSolver)
