from Domain.Puzzles.Snake.SnakeSolver import SnakeSolver
from GridPlayers.GridPuzzle.GridPuzzleSnakePlayer import GridPuzzleSnakePlayer
from GridProviders.GridPuzzle.GridPuzzleSnakeGridProvider import GridPuzzleSnakeGridProvider
from Run.GameRegistry import GameRegistry


def register_snake():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/snake", 
        GridPuzzleSnakeGridProvider, 
        GridPuzzleSnakePlayer
    )(SnakeSolver)