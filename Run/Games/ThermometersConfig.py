from Domain.Puzzles.Thermometers.ThermometersSolver import ThermometersSolver
from GridPlayers.PuzzleMobiles.PuzzleThermometersPlayer import PuzzleThermometersPlayer
from GridProviders.PuzzlesMobile.PuzzleThermometersGridProvider import PuzzleThermometersGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-thermometers\.com", 
        PuzzleThermometersGridProvider, 
        PuzzleThermometersPlayer
    )(ThermometersSolver)