from Domain.Puzzles.Kurodoko.KurodokoSolver import KurodokoSolver
from GridPlayers.PuzzleMobiles.PuzzleKurodokoPlayer import PuzzleKurodokoPlayer
from GridProviders.PuzzlesMobile.PuzzleKurodokoGridProvider import PuzzleKurodokoGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register('kurodoko', KurodokoSolver, PuzzleKurodokoGridProvider, PuzzleKurodokoPlayer)
