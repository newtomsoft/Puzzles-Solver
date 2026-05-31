from PuzzleSolver.Puzzles.Island.IslandSolver import IslandSolver
from GridPlayers.GridPuzzle.GridPuzzleIslandPlayer import GridPuzzleIslandPlayer
from GridProviders.GridPuzzle.GridPuzzleIslandGridProvider import GridPuzzleIslandGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/island", 
        GridPuzzleIslandGridProvider, 
        GridPuzzleIslandPlayer
    )(IslandSolver)
