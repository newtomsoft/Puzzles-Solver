from PuzzleSolver.Puzzles.SheepAndWolves.SheepAndWolvesSolver import SheepAndWolvesSolver
from GridPlayers.GridPuzzle.GridPuzzleSheepAndWolvesPlayer import GridPuzzleSheepAndWolvesPlayer
from GridProviders.GridPuzzle.GridPuzzleSheepAndWolvesGridProvider import GridPuzzleSheepAndWolvesGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/sheep-and-wolves.*",
        GridPuzzleSheepAndWolvesGridProvider,
        GridPuzzleSheepAndWolvesPlayer
    )(SheepAndWolvesSolver)
