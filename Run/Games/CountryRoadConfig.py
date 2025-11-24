from Domain.Puzzles.CountryRoad.CountryRoadSolver import CountryRoadSolver
from GridPlayers.GridPuzzle.GridPuzzleCountryRoadPlayer import GridPuzzleCountryRoadPlayer
from GridProviders.GridPuzzle.GridPuzzleCountryRoadGridProvider import GridPuzzleCountryRoadGridProvider
from Run.GameRegistry import GameRegistry


def register_countryroad():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/country-road", 
        GridPuzzleCountryRoadGridProvider, 
        GridPuzzleCountryRoadPlayer
    )(CountryRoadSolver)