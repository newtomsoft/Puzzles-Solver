import re
import time

from GridProviders.PlaySumpleteGridProvider import PlaySumpleteGridProvider
from GridProviders.PuzzleAkariGridProvider import PuzzleAkariGridProvider
from GridProviders.PuzzleAquariumGridProvider import PuzzleAquariumGridProvider
from GridProviders.PuzzleBimaruGridProvider import PuzzleBimaruGridProvider
from GridProviders.PuzzleBinairoGridProvider import PuzzleBinairoGridProvider
from GridProviders.PuzzleBinairoPlusGridProvider import PuzzleBinairoPlusGridProvider
from GridProviders.PuzzleDominosaGridProvider import PuzzleDominosaGridProvider
from GridProviders.PuzzleFutoshikiGridProvider import PuzzleFutoshikiGridProvider
from GridProviders.PuzzleHitoriGridProvider import PuzzleHitoriGridProvider
from GridProviders.PuzzleKakurasuGridProvider import PuzzleKakurasuGridProvider
from GridProviders.PuzzleKakuroGridProvider import PuzzleKakuroGridProvider
from GridProviders.PuzzleMinesweeperMosaicGridProvider import PuzzleMinesweeperMosaicGridProvider
from GridProviders.PuzzleNonogramGridProvider import PuzzleNonogramGridProvider
from GridProviders.PuzzleNorinoriGridProvider import PuzzleNorinoriGridProvider
from GridProviders.PuzzleNurikabeGridProvider import PuzzleNurikabeGridProvider
from GridProviders.PuzzleRenzokuGridProvider import PuzzleRenzokuGridProvider
from GridProviders.PuzzleShikakuGridProvider import PuzzleShikakuGridProvider
from GridProviders.PuzzleSkyscrapersGridProvider import PuzzleSkyscrapersGridProvider
from GridProviders.PuzzleStarBattleGridProvider import PuzzleStarBattleGridProvider
from GridProviders.PuzzleStitchesGridProvider import PuzzleStitchesGridProvider
from GridProviders.PuzzleSudokuGridProvider import PuzzleSudokuGridProvider
from GridProviders.PuzzleTapaGridProvider import PuzzleTapaGridProvider
from GridProviders.PuzzleTentsGridProvider import PuzzleTentsGridProvider
from GridProviders.QueensGridProvider import QueensGridProvider
from Puzzles.Akari.AkariGame import AkariGame
from Puzzles.Aquarium.AquariumGame import AquariumGame
from Puzzles.Bimaru.BimaruGame import BimaruGame
from Puzzles.Binairo.BinairoGame import BinairoGame
from Puzzles.BinairoPlus.BinairoPlusGame import BinairoPlusGame
from Puzzles.Dominosa.DominosaGame import DominosaGame
from Puzzles.Futoshiki.FutoshikiGame import FutoshikiGame
from Puzzles.Hitori.HitoriGame import HitoriGame
from Puzzles.Kakurasu.KakurasuGame import KakurasuGame
from Puzzles.Kakuro.KakuroGame import KakuroGame
from Puzzles.MinesweeperMosaic.MinesweeperMosaicGame import MinesweeperMosaicGame
from Puzzles.Nonogram.NonogramGame import NonogramGame
from Puzzles.Norinori.NorinoriGame import NorinoriGame
from Puzzles.Nurikabe.NurikabeGame import NurikabeGame
from Puzzles.Queens.QueensGame import QueensGame
from Puzzles.Renzoku.RenzokuGame import RenzokuGame
from Puzzles.Shikaku.ShikakuGame import ShikakuGame
from Puzzles.Skyscrapers.SkyscrapersGame import SkyscrapersGame
from Puzzles.Stitches.StitchesGame import StitchesGame
from Puzzles.Sudoku.SudokuGame import SudokuGame
from Puzzles.Sumplete.SumpleteGame import SumpleteGame
from Puzzles.Tapa.TapaGame import TapaGame
from Puzzles.Tents.TentsGame import TentsGame
from Utils.Grid import Grid


class PuzzleMainConsole:
    @staticmethod
    def main():
        puzzle_game, data_game = PuzzleMainConsole.get_game_and_grid()
        PuzzleMainConsole.run(puzzle_game, data_game)

    @staticmethod
    def get_game_and_grid():
        print("Puzzle Game")
        print("Enter url")
        console_input = input()
        if console_input == "queens":
            console_input = "https://www.linkedin.com/games/queens/"

        url_patterns = {
            r"https://.*\.puzzle-light-up\.com": (AkariGame, PuzzleAkariGridProvider),
            r"https://.*\.puzzle-aquarium\.com": (AquariumGame, PuzzleAquariumGridProvider),
            r"https://.*\.puzzle-battleships\.com": (BimaruGame, PuzzleBimaruGridProvider),
            r"https://.*\.puzzle-binairo\.com/.*binairo-plus": (BinairoPlusGame, PuzzleBinairoPlusGridProvider),
            r"https://.*\.puzzle-binairo\.com": (BinairoGame, PuzzleBinairoGridProvider),
            r"https://.*\.puzzle-dominosa\.com": (DominosaGame, PuzzleDominosaGridProvider),
            r"https://.*\.puzzle-futoshiki\.com/.*renzoku": (RenzokuGame, PuzzleRenzokuGridProvider),
            r"https://.*\.puzzle-futoshiki\.com": (FutoshikiGame, PuzzleFutoshikiGridProvider),
            r"https://.*\.puzzle-hitori\.com": (HitoriGame, PuzzleHitoriGridProvider),
            r"https://.*\.puzzle-kakurasu\.com": (KakurasuGame, PuzzleKakurasuGridProvider),
            r"https://.*\.puzzle-kakuro\.com": (KakuroGame, PuzzleKakuroGridProvider),
            r"https://.*\.puzzle-minesweeper\.com/.*mosaic": (MinesweeperMosaicGame, PuzzleMinesweeperMosaicGridProvider),
            r"https://.*\.puzzle-nonograms\.com": (NonogramGame, PuzzleNonogramGridProvider),
            r"https://.*\.puzzle-norinori\.com": (NorinoriGame, PuzzleNorinoriGridProvider),
            r"https://.*\.puzzle-nurikabe\.com": (NurikabeGame, PuzzleNurikabeGridProvider),
            r"https://www\.linkedin\.com/games/queens": (QueensGame, QueensGridProvider),
            r"https://.*\.puzzle-star-battle\.com": (QueensGame, PuzzleStarBattleGridProvider),
            r"https://.*\.puzzle-shikaku\.com": (ShikakuGame, PuzzleShikakuGridProvider),
            r"https://.*\.puzzle-skyscrapers\.com": (SkyscrapersGame, PuzzleSkyscrapersGridProvider),
            r"https://.*\.puzzle-stitches\.com": (StitchesGame, PuzzleStitchesGridProvider),
            r"https://.*\.puzzle-sudoku\.com": (SudokuGame, PuzzleSudokuGridProvider),
            r"https://playsumplete\.com/": (SumpleteGame, PlaySumpleteGridProvider),
            r"https://.*\.puzzle-tapa\.com": (TapaGame, PuzzleTapaGridProvider),
            r"https://.*\.puzzle-tents\.com": (TentsGame, PuzzleTentsGridProvider),
        }
        for pattern, (game_class, provider_class) in url_patterns.items():
            if re.match(pattern, console_input):
                game = game_class
                provider = provider_class()
                return game, provider.get_grid(console_input)
        raise ValueError("No grid provider found")

    @staticmethod
    def run(puzzle_game, data_game):
        if type(data_game) is tuple:
            grid, *extra_data = data_game
            game = puzzle_game(grid, *extra_data)
        else:
            game = puzzle_game(data_game)
        start_time = time.time()
        solution_grid = game.get_solution()
        end_time = time.time()
        execution_time = end_time - start_time
        if solution_grid != Grid.empty():
            print(f"Solution found in {execution_time:.2f} seconds")
            print(solution_grid.to_console_string())
        else:
            print(f"No solution found")


if __name__ == '__main__':
    PuzzleMainConsole.main()
