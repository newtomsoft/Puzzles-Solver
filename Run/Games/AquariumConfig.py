from Domain.Puzzles.Aquarium.AquariumSolver import AquariumSolver
from GridPlayers.PuzzleMobiles.PuzzleAquariumPlayer import PuzzleAquariumPlayer
from GridProviders.PuzzlesMobile.PuzzleAquariumGridProvider import PuzzleAquariumGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-aquarium\.com", 
        PuzzleAquariumGridProvider, 
        PuzzleAquariumPlayer
    )(AquariumSolver)