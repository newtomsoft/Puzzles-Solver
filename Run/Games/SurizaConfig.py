from Domain.Puzzles.Suriza.SurizaSolver import SurizaSolver
from GridPlayers.GridPuzzle.GridPuzzleSlitherlinkPlayer import GridPuzzleSlitherlinkPlayer
from GridPlayers.PuzzleMobiles.PuzzleMasyuPlayer import PuzzleMasyuPlayer
from GridProviders.GridPuzzle.GridPuzzleSlitherlinkGridProvider import GridPuzzleSlitherlinkGridProvider
from GridProviders.PuzzlesMobile.PuzzleSurizaGridProvider import PuzzleSurizaGridProvider
from Run.GameRegistry import GameRegistry


def register_suriza():
    GameRegistry.register_game(
        r"https://.*gridpuzzle\.com/slitherlink", 
        GridPuzzleSlitherlinkGridProvider, 
        GridPuzzleSlitherlinkPlayer
    )(SurizaSolver)

    GameRegistry.register_game(
        r"https://.*\.puzzle-loop\.com", 
        PuzzleSurizaGridProvider, 
        PuzzleMasyuPlayer
    )(SurizaSolver)