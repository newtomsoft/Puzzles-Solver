from Domain.Puzzles.Kemaru.KemaruSolver import KemaruSolver
from GridPlayers.VingtMinutes.VingtMinutesKemaruPlayer import VingtMinutesKemaruPlayer
from GridProviders.VingtMinutes.VingtMinutesKemaruGridProvider import VingtMinutesKemaruGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://www\.20minutes\.fr/services/jeux/kemaru", 
        VingtMinutesKemaruGridProvider, 
        VingtMinutesKemaruPlayer
    )(KemaruSolver)