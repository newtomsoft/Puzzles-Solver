from Domain.Puzzles.RoundTrip.RoundTripSolver import RoundTripSolver
from GridPlayers.GridPuzzle.GridPuzzleRoundTripPlayer import GridPuzzleRoundTripPlayer
from GridProviders.GridPuzzle.GridPuzzleRoundTripGridProvider import GridPuzzleRoundTripGridProvider
from Run.GameRegistry import GameRegistry


def register_roundtrip():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/round-trip", 
        GridPuzzleRoundTripGridProvider, 
        GridPuzzleRoundTripPlayer
    )(RoundTripSolver)