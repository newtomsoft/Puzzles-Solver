from PuzzleSolver.Puzzles.RabbitsAndTrees.RabbitsAndTreesSolver import RabbitsAndTreesSolver
from GridPlayers.GridPuzzle.GridPuzzleRabbitsAndTreesPlayer import GridPuzzleRabbitsAndTreesPlayer
from GridProviders.GridPuzzle.GridPuzzleRabbitsAndTreesGridProvider import GridPuzzleRabbitsAndTreesGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/rabbits-and-trees",
        GridPuzzleRabbitsAndTreesGridProvider,
        GridPuzzleRabbitsAndTreesPlayer
    )(RabbitsAndTreesSolver)
