from Domain.Puzzles.StarBattle.StarBattleSolver import StarBattleSolver
from GridPlayers.GridPuzzle.GridPuzzleStarBattlePlayer import GridPuzzleStarBattlePlayer
from GridPlayers.LinkedIn.QueensPlayer import QueensPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronStarBattleGridPlayer import PuzzleBaronStarBattlePlayer
from GridPlayers.PuzzleMobiles.PuzzleStarBattlePlayer import PuzzleStarBattlePlayer
from GridProviders.GridPuzzle.GridPuzzleStarBattleGridProvider import GridPuzzleStarBattleGridProvider
from GridProviders.Linkedin.QueensGridProvider import QueensGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronStarBattleGridProvider import PuzzleBaronStarBattleGridProvider
from GridProviders.PuzzlesMobile.PuzzleStarBattleGridProvider import PuzzleStarBattleGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*\.puzzle-star-battle\.com", 
        PuzzleStarBattleGridProvider, 
        PuzzleStarBattlePlayer
    )(StarBattleSolver)

    GameRegistry.register(
        r"https://.*gridpuzzle\.com/starbattle", 
        GridPuzzleStarBattleGridProvider, 
        GridPuzzleStarBattlePlayer
    )(StarBattleSolver)

    GameRegistry.register(
        r"https://starbattle\.puzzlebaron\.com/init2\.php", 
        PuzzleBaronStarBattleGridProvider, 
        PuzzleBaronStarBattlePlayer
    )(StarBattleSolver)

    GameRegistry.register(
        r"https://www\.linkedin\.com/games/queens", 
        QueensGridProvider, 
        QueensPlayer
    )(StarBattleSolver)