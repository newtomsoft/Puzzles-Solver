from Domain.Puzzles.Sumplete.SumpleteSolver import SumpleteSolver
from GridProviders.PlaySumplete.PlaySumpleteGridProvider import PlaySumpleteGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://playsumplete\.com/", 
        PlaySumpleteGridProvider, 
        None
    )(SumpleteSolver)