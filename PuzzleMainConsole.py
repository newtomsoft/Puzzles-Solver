import re
import time
from typing import Tuple, Any

from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Akari.AkariSolver import AkariSolver
from Domain.Puzzles.Aquarium.AquariumSolver import AquariumSolver
from Domain.Puzzles.Bimaru.BimaruSolver import BimaruSolver
from Domain.Puzzles.Binairo.BinairoSolver import BinairoSolver
from Domain.Puzzles.BinairoPlus.BinairoPlusSolver import BinairoPlusSolver
from Domain.Puzzles.Dominosa.DominosaSolver import DominosaSolver
from Domain.Puzzles.Futoshiki.FutoshikiSolver import FutoshikiSolver
from Domain.Puzzles.GameSolver import GameSolver
from Domain.Puzzles.Hashi.HashiSolver import HashiSolver
from Domain.Puzzles.Heyawake.HeyawakeSolver import HeyawakeSolver
from Domain.Puzzles.Hitori.HitoriSolver import HitoriSolver
from Domain.Puzzles.Kakurasu.KakurasuSolver import KakurasuSolver
from Domain.Puzzles.Kakuro.KakuroSolver import KakuroSolver
from Domain.Puzzles.KenKen.KenKenSolver import KenKenSolver
from Domain.Puzzles.Lits.LitsSolver import LitsSolver
from Domain.Puzzles.Masyu.MasyuSolver import MasyuSolver
from Domain.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver
from Domain.Puzzles.MinesweeperMosaic.MinesweeperMosaicSolver import MinesweeperMosaicSolver
from Domain.Puzzles.Nonogram.NonogramSolver import NonogramSolver
from Domain.Puzzles.Norinori.NorinoriSolver import NorinoriSolver
from Domain.Puzzles.NumberLink.NumberLinkSolver import NumberLinkSolver
from Domain.Puzzles.Nurikabe.NurikabeSolver import NurikabeSolver
from Domain.Puzzles.Pipes.PipesSolver import PipesSolver
from Domain.Puzzles.PipesWrap.PipesWrapSolver import PipesWrapSolver
from Domain.Puzzles.Renzoku.RenzokuSolver import RenzokuSolver
from Domain.Puzzles.Shikaku.ShikakuSolver import ShikakuSolver
from Domain.Puzzles.Shingoki.ShingokiSolver import ShingokiSolver
from Domain.Puzzles.Skyscrapers.SkyscrapersSolver import SkyscrapersSolver
from Domain.Puzzles.Snake.SnakeSolver import SnakeSolver
from Domain.Puzzles.StarBattle.StarBattleSolver import StarBattleSolver
from Domain.Puzzles.Stitches.StitchesSolver import StitchesSolver
from Domain.Puzzles.Sudoku.JigsawSudoku.JigsawSudokuSolver import JigsawSudokuSolver
from Domain.Puzzles.Sudoku.KillerSudoku.KillerSudokuSolver import KillerSudokuSolver
from Domain.Puzzles.Sudoku.Sudoku.SudokuSolver import SudokuSolver
from Domain.Puzzles.Sumplete.SumpleteSolver import SumpleteSolver
from Domain.Puzzles.Suriza.SurizaSolver import SurizaSolver
from Domain.Puzzles.Tapa.TapaSolver import TapaSolver
from Domain.Puzzles.TentaiShow.TentaiShowSolver import TentaiShowSolver
from Domain.Puzzles.Tents.TentsSolver import TentsSolver
from Domain.Puzzles.Thermometers.ThermometersSolver import ThermometersSolver
from Domain.Puzzles.Vectors.VectorsSolver import VectorsSolver
from Domain.Puzzles.YinYang.YinYangSolver import YinYangSolver
from Domain.Puzzles.Zip.ZipSolver import ZipSolver
from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.GridPuzzle.GridPuzzleShingokiGridPlayer import GridPuzzleShingokiGridPlayer
from GridPlayers.GridPuzzle.GridPuzzleSnakeGridPlayer import GridPuzzleSnakeGridPlayer
from GridPlayers.GridPuzzle.GridPuzzleStr8tsGridPlayer import GridPuzzleStr8tsGridPlayer
from GridPlayers.LinkedIn.ZipGridPlayer import ZipGridPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronCalcudokuGridPlayer import PuzzleBaronCalcudokuGridPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronCampsitesGridPlayer import PuzzleBaronCampsitesGridPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronLaserGridsGridPlayer import PuzzleBaronLaserGridsGridPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronNumberLinksGridPlayer import PuzzleBaronNumberLinksGridPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronStarBattleGridPlayer import PuzzleBaronStarBattleGridPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronVectorsGridPlayer import PuzzleBaronVectorsGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleAkariGridPlayer import PuzzleAkariGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleAquariumGridPlayer import PuzzleAquariumGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleBimaruGridPlayer import PuzzleBimaruGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleBinairoGridPlayer import PuzzleBinairoGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleDominosaGridPlayer import PuzzleDominosaGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleFutoshikiGridPlayer import PuzzleFutoshikiGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleHashiGridPlayer import PuzzleHashiGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleHeyawakeGridPlayer import PuzzleHeyawakeGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleHitoriGridPlayer import PuzzleHitoriGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleKakurasuGridPlayer import PuzzleKakurasuGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleKakuroGridPlayer import PuzzleKakuroGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleLitsGridPlayer import PuzzleLitsGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleMasyuGridPlayer import PuzzleMasyuGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleMinesweeperGridPlayer import PuzzleMinesweeperGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleMinesweeperMosaicGridPlayer import PuzzleMinesweeperMosaicGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleNonogramsGridPlayer import PuzzleNonogramsGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleNorinoriGridPlayer import PuzzleNorinoriGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleNurikabeGridPlayer import PuzzleNurikabeGridPlayer
from GridPlayers.PuzzleMobiles.PuzzlePipesGridPlayer import PuzzlePipesGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleShikakuGridPlayer import PuzzleShikakuGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleSkyscrapersGridPlayer import PuzzleSkyScrapersGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleStarBattleGridPlayer import PuzzleStarBattleGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleStitchesGridPlayer import PuzzleStitchesGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleSudokuGridPlayer import PuzzleSudokuGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleTapaGridPlayer import PuzzleTapaGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleTentsGridPlayer import PuzzleTentsGridPlayer
from GridPlayers.PuzzleMobiles.PuzzleThermometersGridPlayer import PuzzleThermometersGridPlayer
from GridProviders.EscapeSudoku.EscapeSudokuProvider import EscapeSudokuGridProvider
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleShingokiGridProvider import GridPuzzleShingokiGridProvider
from GridProviders.GridPuzzle.GridPuzzleSnakeGridProvider import GridPuzzleSnakeGridProvider
from GridProviders.GridPuzzle.GridPuzzleStr8tsGridProvider import GridPuzzleStr8tsGridProvider
from GridProviders.Linkedin.QueensGridProvider import QueensGridProvider
from GridProviders.Linkedin.ZipGridProvider import ZipGridProvider
from GridProviders.PlaySumplete.PlaySumpleteGridProvider import PlaySumpleteGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronCalcudokuGridProvider import PuzzleBaronCalcudokuGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronCampsitesGridProvider import PuzzleBaronCampsitesGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronLaserGridsGridProvider import PuzzleBaronLaserGridsGridProvider
from GridProviders.PuzzleBaron.PuzzleBaronNumberLinksGridProvider import PuzzleBaronNumberLinksGridProvider
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
from Puzzles.Str8ts.Str8tsSolver import Str8tsSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine

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
            r"https://lasergrids\.puzzlebaron\.com/init2\.php": (AkariSolver, PuzzleBaronLaserGridsGridProvider, PuzzleBaronLaserGridsGridPlayer),
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
            r"https://calcudoku\.puzzlebaron\.com/init2\.php": (KenKenSolver, PuzzleBaronCalcudokuGridProvider, PuzzleBaronCalcudokuGridPlayer),
            r"https://.*\.puzzle-killer-sudoku\.com": (KillerSudokuSolver, PuzzleKillerSudokuGridProvider, PuzzleSudokuGridPlayer),  # same player as Sudoku
            r"https://.*\.puzzle-lits\.com": (LitsSolver, PuzzleLitsGridProvider, PuzzleLitsGridPlayer),
            r"https://.*\.puzzle-masyu\.com": (MasyuSolver, PuzzleMasyuGridProvider, PuzzleMasyuGridPlayer),
            r"https://.*\.puzzle-minesweeper\.com/.*mosaic": (MinesweeperMosaicSolver, PuzzleMinesweeperMosaicGridProvider, PuzzleMinesweeperMosaicGridPlayer),
            r"https://.*\.puzzle-minesweeper\.com": (MinesweeperSolver, PuzzleMinesweeperMosaicGridProvider, PuzzleMinesweeperGridPlayer),
            r"https://.*\.puzzle-nonograms\.com": (NonogramSolver, PuzzleNonogramGridProvider, PuzzleNonogramsGridPlayer),
            r"https://.*\.puzzle-norinori\.com": (NorinoriSolver, PuzzleNorinoriGridProvider, PuzzleNorinoriGridPlayer),
            r"https://numberlinks\.puzzlebaron\.com/init2\.php": (NumberLinkSolver, PuzzleBaronNumberLinksGridProvider, PuzzleBaronNumberLinksGridPlayer),
            r"https://.*\.puzzle-nurikabe\.com": (NurikabeSolver, PuzzleNurikabeGridProvider, PuzzleNurikabeGridPlayer),
            r"https://.*\.puzzle-pipes\.com/\?size=\d{2,}": (PipesWrapSolver, PuzzlePipesGridProvider, PuzzlePipesGridPlayer),  # same player and same grid provider as pipes
            r"https://.*\.puzzle-pipes\.com": (PipesSolver, PuzzlePipesGridProvider, PuzzlePipesGridPlayer),
            r"https://.*\.puzzle-shikaku\.com": (ShikakuSolver, PuzzleShikakuGridProvider, PuzzleShikakuGridPlayer),
            r"https://.*\.puzzle-shingoki\.com": (ShingokiSolver, PuzzleShingokiGridProvider, PuzzleMasyuGridPlayer),  # same player as masyu
            r"https://.*gridpuzzle\.com/traffic-lights": (ShingokiSolver, GridPuzzleShingokiGridProvider, GridPuzzleShingokiGridPlayer),
            r"https://.*\.puzzle-skyscrapers\.com": (SkyscrapersSolver, PuzzleSkyscrapersGridProvider, PuzzleSkyScrapersGridPlayer),
            r"https://.*gridpuzzle\.com/snake": (SnakeSolver, GridPuzzleSnakeGridProvider, GridPuzzleSnakeGridPlayer),
            r"https://.*\.puzzle-star-battle\.com": (StarBattleSolver, PuzzleStarBattleGridProvider, PuzzleStarBattleGridPlayer),
            r"https://starbattle\.puzzlebaron\.com/init2\.php": (StarBattleSolver, PuzzleBaronStarBattleGridProvider, PuzzleBaronStarBattleGridPlayer),
            r"https://www\.linkedin\.com/games/queens": (StarBattleSolver, QueensGridProvider, None),
            r"https://.*\.puzzle-stitches\.com": (StitchesSolver, PuzzleStitchesGridProvider, PuzzleStitchesGridPlayer),
            r"https://.*gridpuzzle\.com/str8ts.": (Str8tsSolver, GridPuzzleStr8tsGridProvider, GridPuzzleStr8tsGridPlayer),
            r"https://.*\.puzzle-sudoku\.com": (SudokuSolver, PuzzleSudokuGridProvider, PuzzleSudokuGridPlayer),
            r"https://escape-sudoku.com/": (SudokuSolver, EscapeSudokuGridProvider, None),
            r"https://.*\.puzzle-loop\.com": (SurizaSolver, PuzzleSurizaGridProvider, PuzzleMasyuGridPlayer),  # same player as masyu
            r"https://playsumplete\.com/": (SumpleteSolver, PlaySumpleteGridProvider, None),
            r"https://.*\.puzzle-tapa\.com": (TapaSolver, PuzzleTapaGridProvider, PuzzleTapaGridPlayer),
            r"https://.*\.puzzle-galaxies\.com": (TentaiShowSolver, PuzzleTentaiShowGridProvider, None),
            r"https://.*\.puzzle-tents\.com": (TentsSolver, PuzzleTentsGridProvider, PuzzleTentsGridPlayer),
            r"https://campsites\.puzzlebaron\.com/init2\.php": (TentsSolver, PuzzleBaronCampsitesGridProvider, PuzzleBaronCampsitesGridPlayer),
            r"https://.*\.puzzle-thermometers\.com": (ThermometersSolver, PuzzleThermometersGridProvider, PuzzleThermometersGridPlayer),
            r"https://vectors\.puzzlebaron\.com/init2\.php": (VectorsSolver, PuzzleBaronVectorsGridProvider, PuzzleBaronVectorsGridPlayer),
            r"https://.*\.puzzle-yin-yang\.com": (YinYangSolver, PuzzleYinYangGridProvider, PuzzleBinairoGridPlayer),  # same player as binairo
            r"https://www\.linkedin\.com/games/zip": (ZipSolver, ZipGridProvider, ZipGridPlayer),
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
