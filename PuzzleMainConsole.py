import re
import time
from typing import Tuple, Any

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleAkariGridPlayer import PuzzleAkariGridPlayer
from GridPlayers.PuzzleAquariumGridPlayer import PuzzleAquariumGridPlayer
from GridPlayers.PuzzleBaronAkariGridPlayer import PuzzleBaronAkariGridPlayer
from GridPlayers.PuzzleBaronKenKenGridPlayer import PuzzleBaronKenKenGridPlayer
from GridPlayers.PuzzleBaronStarBattleGridPlayer import PuzzleBaronStarBattleGridPlayer
from GridPlayers.PuzzleBaronVectorsGridPlayer import PuzzleBaronVectorsGridPlayer
from GridPlayers.PuzzleBimaruGridPlayer import PuzzleBimaruGridPlayer
from GridPlayers.PuzzleBinairoGridPlayer import PuzzleBinairoGridPlayer
from GridPlayers.PuzzleDominosaGridPlayer import PuzzleDominosaGridPlayer
from GridPlayers.PuzzleFutoshikiGridPlayer import PuzzleFutoshikiGridPlayer
from GridPlayers.PuzzleHashiGridPlayer import PuzzleHashiGridPlayer
from GridPlayers.PuzzleHeyawakeGridPlayer import PuzzleHeyawakeGridPlayer
from GridPlayers.PuzzleHitoriGridPlayer import PuzzleHitoriGridPlayer
from GridPlayers.PuzzleKakurasuGridPlayer import PuzzleKakurasuGridPlayer
from GridPlayers.PuzzleKakuroGridPlayer import PuzzleKakuroGridPlayer
from GridPlayers.PuzzleLitsGridPlayer import PuzzleLitsGridPlayer
from GridPlayers.PuzzleMasyuGridPlayer import PuzzleMasyuGridPlayer
from GridPlayers.PuzzleMinesweeperGridPlayer import PuzzleMinesweeperGridPlayer
from GridPlayers.PuzzleMinesweeperMosaicGridPlayer import PuzzleMinesweeperMosaicGridPlayer
from GridPlayers.PuzzleNonogramsGridPlayer import PuzzleNonogramsGridPlayer
from GridPlayers.PuzzleNorinoriGridPlayer import PuzzleNorinoriGridPlayer
from GridPlayers.PuzzleNurikabeGridPlayer import PuzzleNurikabeGridPlayer
from GridPlayers.PuzzlePipesGridPlayer import PuzzlePipesGridPlayer
from GridPlayers.PuzzleShikakuGridPlayer import PuzzleShikakuGridPlayer
from GridPlayers.PuzzleSkyscrapersGridPlayer import PuzzleSkyScrapersGridPlayer
from GridPlayers.PuzzleStarBattleGridPlayer import PuzzleStarBattleGridPlayer
from GridPlayers.PuzzleStitchesGridPlayer import PuzzleStitchesGridPlayer
from GridPlayers.PuzzleSudokuGridPlayer import PuzzleSudokuGridPlayer
from GridPlayers.PuzzleTapaGridPlayer import PuzzleTapaGridPlayer
from GridPlayers.PuzzleTentsGridPlayer import PuzzleTentsGridPlayer
from GridPlayers.PuzzleThermometersGridPlayer import PuzzleThermometersGridPlayer
from GridProviders.GridProvider import GridProvider
from GridProviders.Linkedin.QueensGridProvider import QueensGridProvider
from GridProviders.PlaySumplete.PlaySumpleteGridProvider import PlaySumpleteGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronAkariGridProvider import PuzzleBaronAkariGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronKenKenGridProvider import PuzzleBaronKenKenGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronStarBattleGridProvider import PuzzleBaronStarBattleGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronVectorsGridProvider import PuzzleBaronVectorsGridProvider
from GridProviders.PuzzlesMobile.PuzzleAkariGridProvider import PuzzleAkariGridProvider
from GridProviders.PuzzlesMobile.PuzzleAquariumGridProvider import PuzzleAquariumGridProvider
from GridProviders.PuzzlesMobile.PuzzleBimaruGridProvider import PuzzleBimaruGridProvider
from GridProviders.PuzzlesMobile.PuzzleBinairoGridProvider import PuzzleBinairoGridProvider
from GridProviders.PuzzlesMobile.PuzzleBinairoPlusGridProvider import PuzzleBinairoPlusGridProvider
from GridProviders.PuzzlesMobile.PuzzleDominosaGridProvider import PuzzleDominosaGridProvider
from GridProviders.PuzzlesMobile.PuzzleFutoshikiGridProvider import PuzzleFutoshikiGridProvider
from GridProviders.PuzzlesMobile.PuzzleHashiGridProvider import PuzzleHashiGridProvider
from GridProviders.PuzzlesMobile.PuzzleHeyawakeGridProvider import PuzzleHeyawakeGridProvider
from GridProviders.PuzzlesMobile.PuzzleHitoriGridProvider import PuzzleHitoriGridProvider
from GridProviders.PuzzlesMobile.PuzzleJigsawSudokuGridProvider import PuzzleJigsawSudokuGridProvider
from GridProviders.PuzzlesMobile.PuzzleKakurasuGridProvider import PuzzleKakurasuGridProvider
from GridProviders.PuzzlesMobile.PuzzleKakuroGridProvider import PuzzleKakuroGridProvider
from GridProviders.PuzzlesMobile.PuzzleKillerSudokuGridProvider import PuzzleKillerSudokuGridProvider
from GridProviders.PuzzlesMobile.PuzzleLitsGridProvider import PuzzleLitsGridProvider
from GridProviders.PuzzlesMobile.PuzzleMasyuGridProvider import PuzzleMasyuGridProvider
from GridProviders.PuzzlesMobile.PuzzleMinesweeperMosaicGridProvider import PuzzleMinesweeperMosaicGridProvider
from GridProviders.PuzzlesMobile.PuzzleNonogramGridProvider import PuzzleNonogramGridProvider
from GridProviders.PuzzlesMobile.PuzzleNorinoriGridProvider import PuzzleNorinoriGridProvider
from GridProviders.PuzzlesMobile.PuzzleNurikabeGridProvider import PuzzleNurikabeGridProvider
from GridProviders.PuzzlesMobile.PuzzlePipesGridProvider import PuzzlePipesGridProvider
from GridProviders.PuzzlesMobile.PuzzleRenzokuGridProvider import PuzzleRenzokuGridProvider
from GridProviders.PuzzlesMobile.PuzzleShikakuGridProvider import PuzzleShikakuGridProvider
from GridProviders.PuzzlesMobile.PuzzleShingokiGridProvider import PuzzleShingokiGridProvider
from GridProviders.PuzzlesMobile.PuzzleSkyscrapersGridProvider import PuzzleSkyscrapersGridProvider
from GridProviders.PuzzlesMobile.PuzzleStarBattleGridProvider import PuzzleStarBattleGridProvider
from GridProviders.PuzzlesMobile.PuzzleStitchesGridProvider import PuzzleStitchesGridProvider
from GridProviders.PuzzlesMobile.PuzzleSudokuGridProvider import PuzzleSudokuGridProvider
from GridProviders.PuzzlesMobile.PuzzleSurizaGridProvider import PuzzleSurizaGridProvider
from GridProviders.PuzzlesMobile.PuzzleTapaGridProvider import PuzzleTapaGridProvider
from GridProviders.PuzzlesMobile.PuzzleTentaiShowGridProvider import PuzzleTentaiShowGridProvider
from GridProviders.PuzzlesMobile.PuzzleTentsGridProvider import PuzzleTentsGridProvider
from GridProviders.PuzzlesMobile.PuzzleThermometersGridProvider import PuzzleThermometersGridProvider
from GridProviders.PuzzlesMobile.PuzzleYinYangGridProvider import PuzzleYinYangGridProvider
from Heyawake.HeyawakeSolver import HeyawakeSolver
from KenKen.KenKenSolver import KenKenSolver
from Lits.LitsSolver import LitsSolver
from Pipes.PipesSolver import PipesSolver
from PipesWrap.PipesWrapSolver import PipesWrapSolver
from Puzzles.Akari.AkariSolver import AkariSolver
from Puzzles.Aquarium.AquariumSolver import AquariumSolver
from Puzzles.Bimaru.BimaruSolver import BimaruSolver
from Puzzles.Binairo.BinairoSolver import BinairoSolver
from Puzzles.BinairoPlus.BinairoPlusSolver import BinairoPlusSolver
from Puzzles.Dominosa.DominosaSolver import DominosaSolver
from Puzzles.Futoshiki.FutoshikiSolver import FutoshikiSolver
from Puzzles.GameSolver import GameSolver
from Puzzles.Hashi.HashiSolver import HashiSolver
from Puzzles.Hitori.HitoriSolver import HitoriSolver
from Puzzles.Kakurasu.KakurasuSolver import KakurasuSolver
from Puzzles.Kakuro.KakuroSolver import KakuroSolver
from Puzzles.Masyu.MasyuSolver import MasyuSolver
from Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver
from Puzzles.MinesweeperMosaic.MinesweeperMosaicSolver import MinesweeperMosaicSolver
from Puzzles.Nonogram.NonogramSolver import NonogramSolver
from Puzzles.Norinori.NorinoriSolver import NorinoriSolver
from Puzzles.Nurikabe.NurikabeSolver import NurikabeSolver
from Puzzles.Renzoku.RenzokuSolver import RenzokuSolver
from Puzzles.Shikaku.ShikakuSolver import ShikakuSolver
from Puzzles.Shingoki.ShingokiSolver import ShingokiSolver
from Puzzles.Skyscrapers.SkyscrapersSolver import SkyscrapersSolver
from Puzzles.Stitches.StitchesSolver import StitchesSolver
from Puzzles.Sudoku.JigsawSudoku.JigsawSudokuSolver import JigsawSudokuSolver
from Puzzles.Sudoku.KillerSudoku.KillerSudokuSolver import KillerSudokuSolver
from Puzzles.Sudoku.Sudoku.SudokuSolver import SudokuSolver
from Puzzles.Sumplete.SumpleteSolver import SumpleteSolver
from Puzzles.Suriza.SurizaSolver import SurizaSolver
from Puzzles.Tapa.TapaSolver import TapaSolver
from Puzzles.TentaiShow.TentaiShowSolver import TentaiShowSolver
from Puzzles.Tents.TentsSolver import TentsSolver
from Puzzles.Thermometers.ThermometersSolver import ThermometersSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from StarBattle.StarBattleSolver import StarBattleSolver
from Utils.Grid import Grid
from Vectors.VectorsSolver import VectorsSolver
from YinYang.YinYangSolver import YinYangSolver

SOLVER_ENGINE = Z3SolverEngine()


class PuzzleMainConsole:
    @staticmethod
    def main():
        game_solver, data_game, browser, game_player = PuzzleMainConsole.get_game_data_player()
        solution = PuzzleMainConsole.run(game_solver, data_game)
        if game_player is not None and solution != Grid.empty():
            game_player.play(solution, browser)

    @staticmethod
    def get_game_data_player() -> Tuple[GameSolver, Any, BrowserContext, GridPlayer | None]:
        print("Puzzle Solver")
        print("Enter game url")
        console_input = input()
        if console_input == "queens":
            console_input = "https://www.linkedin.com/games/queens/"

        url_patterns = {
            r"https://.*\.puzzle-light-up\.com": (AkariSolver, PuzzleAkariGridProvider, PuzzleAkariGridPlayer),
            r"https://lasergrids\.puzzlebaron\.com/init2\.php": (AkariSolver, PuzzleBaronAkariGridProvider, PuzzleBaronAkariGridPlayer),
            r"https://.*\.puzzle-aquarium\.com": (AquariumSolver, PuzzleAquariumGridProvider, PuzzleAquariumGridPlayer),
            r"https://.*\.puzzle-battleships\.com": (BimaruSolver, PuzzleBimaruGridProvider, PuzzleBimaruGridPlayer),
            r"https://.*\.puzzle-binairo\.com/.*binairo-plus": (BinairoPlusSolver, PuzzleBinairoPlusGridProvider, PuzzleBinairoGridPlayer),  # same player as binairo
            r"https://.*\.puzzle-binairo\.com": (BinairoSolver, PuzzleBinairoGridProvider, PuzzleBinairoGridPlayer),
            r"https://.*\.puzzle-dominosa\.com": (DominosaSolver, PuzzleDominosaGridProvider, PuzzleDominosaGridPlayer),
            r"https://.*\.puzzle-futoshiki\.com/.*renzoku": (RenzokuSolver, PuzzleRenzokuGridProvider, PuzzleFutoshikiGridPlayer),  # same player as futoshiki
            r"https://.*\.puzzle-futoshiki\.com": (FutoshikiSolver, PuzzleFutoshikiGridProvider, PuzzleFutoshikiGridPlayer),
            r"https://.*\.puzzle-bridges\.com": (HashiSolver, PuzzleHashiGridProvider, PuzzleHashiGridPlayer),
            r"https://.*\.puzzle-heyawake\.com": (HeyawakeSolver, PuzzleHeyawakeGridProvider, PuzzleHeyawakeGridPlayer),
            r"https://.*\.puzzle-hitori\.com": (HitoriSolver, PuzzleHitoriGridProvider, PuzzleHitoriGridPlayer),
            r"https://.*\.puzzle-jigsaw-sudoku\.com": (JigsawSudokuSolver, PuzzleJigsawSudokuGridProvider, PuzzleSudokuGridPlayer),  # same player as sudoku
            r"https://.*\.puzzle-kakurasu\.com": (KakurasuSolver, PuzzleKakurasuGridProvider, PuzzleKakurasuGridPlayer),
            r"https://.*\.puzzle-kakuro\.com": (KakuroSolver, PuzzleKakuroGridProvider, PuzzleKakuroGridPlayer),
            r"https://calcudoku\.puzzlebaron\.com/init2\.php": (KenKenSolver, PuzzleBaronKenKenGridProvider, PuzzleBaronKenKenGridPlayer),
            r"https://.*\.puzzle-killer-sudoku\.com": (KillerSudokuSolver, PuzzleKillerSudokuGridProvider, PuzzleSudokuGridPlayer),  # same player as Sudoku
            r"https://.*\.puzzle-lits\.com": (LitsSolver, PuzzleLitsGridProvider, PuzzleLitsGridPlayer),
            r"https://.*\.puzzle-masyu\.com": (MasyuSolver, PuzzleMasyuGridProvider, PuzzleMasyuGridPlayer),
            r"https://.*\.puzzle-minesweeper\.com/.*mosaic": (MinesweeperMosaicSolver, PuzzleMinesweeperMosaicGridProvider, PuzzleMinesweeperMosaicGridPlayer),
            r"https://.*\.puzzle-minesweeper\.com": (MinesweeperSolver, PuzzleMinesweeperMosaicGridProvider, PuzzleMinesweeperGridPlayer),
            r"https://.*\.puzzle-nonograms\.com": (NonogramSolver, PuzzleNonogramGridProvider, PuzzleNonogramsGridPlayer),
            r"https://.*\.puzzle-norinori\.com": (NorinoriSolver, PuzzleNorinoriGridProvider, PuzzleNorinoriGridPlayer),
            r"https://.*\.puzzle-nurikabe\.com": (NurikabeSolver, PuzzleNurikabeGridProvider, PuzzleNurikabeGridPlayer),
            r"https://.*\.puzzle-pipes\.com/\?size=\d{2,}": (PipesWrapSolver, PuzzlePipesGridProvider, PuzzlePipesGridPlayer),  # same player and same grid provider as pipes
            r"https://.*\.puzzle-pipes\.com": (PipesSolver, PuzzlePipesGridProvider, PuzzlePipesGridPlayer),
            r"https://.*\.puzzle-shikaku\.com": (ShikakuSolver, PuzzleShikakuGridProvider, PuzzleShikakuGridPlayer),
            r"https://.*\.puzzle-shingoki\.com": (ShingokiSolver, PuzzleShingokiGridProvider, PuzzleMasyuGridPlayer),  # same player as masyu
            r"https://.*\.puzzle-skyscrapers\.com": (SkyscrapersSolver, PuzzleSkyscrapersGridProvider, PuzzleSkyScrapersGridPlayer),
            r"https://.*\.puzzle-star-battle\.com": (StarBattleSolver, PuzzleStarBattleGridProvider, PuzzleStarBattleGridPlayer),
            r"https://starbattle\.puzzlebaron\.com/init2\.php": (StarBattleSolver, PuzzleBaronStarBattleGridProvider, PuzzleBaronStarBattleGridPlayer),
            r"https://www\.linkedin\.com/games/queens": (StarBattleSolver, QueensGridProvider, None),
            r"https://.*\.puzzle-stitches\.com": (StitchesSolver, PuzzleStitchesGridProvider, PuzzleStitchesGridPlayer),
            r"https://.*\.puzzle-sudoku\.com": (SudokuSolver, PuzzleSudokuGridProvider, PuzzleSudokuGridPlayer),
            r"https://.*\.puzzle-loop\.com": (SurizaSolver, PuzzleSurizaGridProvider, PuzzleMasyuGridPlayer),  # same player as masyu
            r"https://playsumplete\.com/": (SumpleteSolver, PlaySumpleteGridProvider, None),
            r"https://.*\.puzzle-tapa\.com": (TapaSolver, PuzzleTapaGridProvider, PuzzleTapaGridPlayer),
            r"https://.*\.puzzle-galaxies\.com": (TentaiShowSolver, PuzzleTentaiShowGridProvider, None),
            r"https://.*\.puzzle-tents\.com": (TentsSolver, PuzzleTentsGridProvider, PuzzleTentsGridPlayer),
            r"https://.*\.puzzle-thermometers\.com": (ThermometersSolver, PuzzleThermometersGridProvider, PuzzleThermometersGridPlayer),
            r"https://.*\.puzzle-yin-yang\.com": (YinYangSolver, PuzzleYinYangGridProvider, PuzzleBinairoGridPlayer),  # same player as binairo
            r"https://vectors\.puzzlebaron\.com/init2\.php": (VectorsSolver, PuzzleBaronVectorsGridProvider, PuzzleBaronVectorsGridPlayer),
        }
        for pattern, (game_class, grid_provider_class, player_class) in url_patterns.items():
            if re.match(pattern, console_input):
                game_solver: GameSolver = game_class
                grid_provider: GridProvider = grid_provider_class()
                game_player: GridPlayer | None = player_class() if player_class is not None else None
                game_data, browser_context = grid_provider.get_grid(console_input)
                return game_solver, game_data, browser_context, game_player
        raise ValueError("No grid provider found")

    @staticmethod
    def run(puzzle_game: type(GameSolver), data_game):
        if type(data_game) is tuple:
            grid = data_game[0]
            extra_data = data_game[1:]
            game_solver = puzzle_game(grid, *extra_data, SOLVER_ENGINE)
        else:
            game_solver = puzzle_game(data_game, SOLVER_ENGINE)

        start_time = time.time()
        solution = game_solver.get_solution()
        end_time = time.time()
        execution_time = end_time - start_time
        if solution != Grid.empty():
            print(f"Solution found in {execution_time:.2f} seconds")
            print(solution)
            return solution
        else:
            print(f"No solution found")
            return solution


if __name__ == '__main__':
    PuzzleMainConsole.main()
