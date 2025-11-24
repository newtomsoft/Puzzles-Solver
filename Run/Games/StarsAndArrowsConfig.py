from Domain.Puzzles.StarsAndArrows.StarsAndArrowsSolver import StarsAndArrowsSolver
from GridPlayers.GridPuzzle.GridPuzzleStarsAndArrowsPlayer import GridPuzzleStarsAndArrowsPlayer
from GridProviders.GridPuzzle.GridPuzzleStarsAndArrowsGridProvider import GridPuzzleStarsAndArrowsGridProvider
from Run.GameRegistry import GameRegistry


def register_starsandarrows():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/stars-and-arrows", 
        GridPuzzleStarsAndArrowsGridProvider, 
        GridPuzzleStarsAndArrowsPlayer
    )(StarsAndArrowsSolver)