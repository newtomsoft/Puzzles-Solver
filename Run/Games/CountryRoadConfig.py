from Domain.Puzzles.CountryRoad.CountryRoadSolver import CountryRoadSolver
from GridPlayers.GridPuzzle.GridPuzzleCountryRoadPlayer import GridPuzzleCountryRoadPlayer
from GridProviders.GridPuzzle.GridPuzzleCountryRoadGridProvider import GridPuzzleCountryRoadGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/country-road", 
        GridPuzzleCountryRoadGridProvider, 
        GridPuzzleCountryRoadPlayer
    )(CountryRoadSolver)