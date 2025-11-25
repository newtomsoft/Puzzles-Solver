from Domain.Puzzles.Sumplete.SumpleteSolver import SumpleteSolver
from GridProviders.PlaySumplete.PlaySumpleteGridProvider import PlaySumpleteGridProvider
from Run.GameRegistry import GameRegistry


def register_sumplete():
    GameRegistry.register_game(
        r"https://playsumplete\.com/", 
        PlaySumpleteGridProvider, 
        None
    )(SumpleteSolver)