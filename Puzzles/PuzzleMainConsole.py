import time

from PlaySumpleteGridProvider import PlaySumpleteGridProvider
from PuzzleAkariGridProvider import PuzzleAkariGridProvider
from PuzzleAquariumGridProvider import PuzzleAquariumGridProvider
from PuzzleBimaruGridProvider import PuzzleBimaruGridProvider
from PuzzleBinairoGridProvider import PuzzleBinairoGridProvider
from PuzzleBinairoPlusGridProvider import PuzzleBinairoPlusGridProvider
from PuzzleDominosaGridProvider import PuzzleDominosaGridProvider
from PuzzleHitoriGridProvider import PuzzleHitoriGridProvider
from PuzzleKakurasuGridProvider import PuzzleKakurasuGridProvider
from PuzzleKakuroGridProvider import PuzzleKakuroGridProvider
from PuzzleMinesweeperMosaicGridProvider import PuzzleMinesweeperMosaicGridProvider
from PuzzleNonogramGridProvider import PuzzleNonogramGridProvider
from PuzzleNorinoriGridProvider import PuzzleNorinoriGridProvider
from PuzzleNurikabeGridProvider import PuzzleNurikabeGridProvider
from PuzzleShikakuGridProvider import PuzzleShikakuGridProvider
from PuzzleSkyscrapersGridProvider import PuzzleSkyscrapersGridProvider
from PuzzleStarBattleGridProvider import PuzzleStarBattleGridProvider
from PuzzleStitchesGridProvider import PuzzleStitchesGridProvider
from PuzzleSudokuGridProvider import PuzzleSudokuGridProvider
from PuzzleTapaGridProvider import PuzzleTapaGridProvider
from PuzzleTentsGridProvider import PuzzleTentsGridProvider
from Puzzles.Akari.AkariGame import AkariGame
from Puzzles.Aquarium.AquariumGame import AquariumGame
from Puzzles.Bimaru.BimaruGame import BimaruGame
from Puzzles.Binairo.BinairoGame import BinairoGame
from Puzzles.BinairoPlus.BinairoPlusGame import BinairoPlusGame
from Puzzles.Dominosa.DominosaGame import DominosaGame
from Puzzles.Hitori.HitoriGame import HitoriGame
from Puzzles.Kakurasu.KakurasuGame import KakurasuGame
from Puzzles.Kakuro.KakuroGame import KakuroGame
from Puzzles.MinesweeperMosaic.MinesweeperMosaicGame import MinesweeperMosaicGame
from Puzzles.Nonogram.NonogramGame import NonogramGame
from Puzzles.Norinori.NorinoriGame import NorinoriGame
from Puzzles.Nurikabe.NurikabeGame import NurikabeGame
from Puzzles.Queens.QueensGame import QueensGame
from Puzzles.Shikaku.ShikakuGame import ShikakuGame
from Puzzles.Skyscrapers.SkyscrapersGame import SkyscrapersGame
from Puzzles.Stitches.StitchesGame import StitchesGame
from Puzzles.Sudoku.SudokuGame import SudokuGame
from Puzzles.Sumplete.SumpleteGame import SumpleteGame
from Puzzles.Tapa.TapaGame import TapaGame
from Puzzles.Tents.TentsGame import TentsGame
from QueensGridProvider import QueensGridProvider
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
            "https://www.puzzle-light-up.com": (AkariGame, PuzzleAkariGridProvider),
            "https://fr.puzzle-light-up.com": (AkariGame, PuzzleAkariGridProvider),
            "https://www.puzzle-aquarium.com": (AquariumGame, PuzzleAquariumGridProvider),
            "https://fr.puzzle-aquarium.com": (AquariumGame, PuzzleAquariumGridProvider),
            "https://www.puzzle-battleships.com": (BimaruGame, PuzzleBimaruGridProvider),
            "https://fr.puzzle-battleships.com": (BimaruGame, PuzzleBimaruGridProvider),
            "https://www.puzzle-binairo.com": (BinairoGame, PuzzleBinairoGridProvider),
            "https://fr.puzzle-binairo.com": (BinairoGame, PuzzleBinairoGridProvider),
            "https://www.puzzle-binairoplus.com": (BinairoPlusGame, PuzzleBinairoPlusGridProvider),
            "https://fr.puzzle-binairoplus.com": (BinairoPlusGame, PuzzleBinairoPlusGridProvider),
            "https://www.puzzle-dominosa.com": (DominosaGame, PuzzleDominosaGridProvider),
            "https://fr.puzzle-dominosa.com": (DominosaGame, PuzzleDominosaGridProvider),
            # "https://www.puzzle-futoshiki.com": (FutoshikiGame, PuzzleFutoshikiGridProvider),
            # "https://fr.puzzle-futoshiki.com": (FutoshikiGame, PuzzleFutoshikiGridProvider),
            "https://www.puzzle-hitori.com": (HitoriGame, PuzzleHitoriGridProvider),
            "https://fr.puzzle-hitori.com": (HitoriGame, PuzzleHitoriGridProvider),
            "https://www.puzzle-kakurasu.com": (KakurasuGame, PuzzleKakurasuGridProvider),
            "https://fr.puzzle-kakurasu.com": (KakurasuGame, PuzzleKakurasuGridProvider),
            "https://www.puzzle-kakuro.com": (KakuroGame, PuzzleKakuroGridProvider),
            "https://fr.puzzle-kakuro.com": (KakuroGame, PuzzleKakuroGridProvider),
            "https://www.puzzle-minesweeper.com": (MinesweeperMosaicGame, PuzzleMinesweeperMosaicGridProvider),
            "https://fr.puzzle-minesweeper.com": (MinesweeperMosaicGame, PuzzleMinesweeperMosaicGridProvider),
            "https://www.puzzle-nonogram.com": (NonogramGame, PuzzleNonogramGridProvider),
            "https://fr.puzzle-nonogram.com": (NonogramGame, PuzzleNonogramGridProvider),
            "https://www.puzzle-norinori.com": (NorinoriGame, PuzzleNorinoriGridProvider),
            "https://fr.puzzle-norinori.com": (NorinoriGame, PuzzleNorinoriGridProvider),
            "https://www.puzzle-nurikabe.com": (NurikabeGame, PuzzleNurikabeGridProvider),
            "https://fr.puzzle-nurikabe.com": (NurikabeGame, PuzzleNurikabeGridProvider),
            "https://www.linkedin.com/games/queens": (QueensGame, QueensGridProvider),
            "https://www.puzzle-star-battle.com": (QueensGame, PuzzleStarBattleGridProvider),
            "https://fr.puzzle-star-battle.com": (QueensGame, PuzzleStarBattleGridProvider),
            "https://www.puzzle-shikaku.com": (ShikakuGame, PuzzleShikakuGridProvider),
            "https://fr.puzzle-shikaku.com": (ShikakuGame, PuzzleShikakuGridProvider),
            "https://fr.puzzle-skyscrapers.com": (SkyscrapersGame, PuzzleSkyscrapersGridProvider),
            "https://www.puzzle-skyscrapers.com": (SkyscrapersGame, PuzzleSkyscrapersGridProvider),
            "https://www.puzzle-stitches.com": (StitchesGame, PuzzleStitchesGridProvider),
            "https://fr.puzzle-stitches.com": (StitchesGame, PuzzleStitchesGridProvider),
            "https://www.puzzle-sudoku.com": (SudokuGame, PuzzleSudokuGridProvider),
            "https://fr.puzzle-sudoku.com": (SudokuGame, PuzzleSudokuGridProvider),
            "https://playsumplete.com/": (SumpleteGame, PlaySumpleteGridProvider),
            "https://www.puzzle-tapa.com": (TapaGame, PuzzleTapaGridProvider),
            "https://fr.puzzle-tapa.com": (TapaGame, PuzzleTapaGridProvider),
            "https://www.puzzle-tents.com": (TentsGame, PuzzleTentsGridProvider),
            "https://fr.puzzle-tents.com": (TentsGame, PuzzleTentsGridProvider),
        }

        for pattern, (game_class, provider_class) in url_patterns.items():
            if pattern in console_input:
                game = game_class
                provider = provider_class()
                return game, provider.get_grid(console_input)

        raise Exception("No provider found")

    @staticmethod
    def run(puzzle_game, data_game):
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
