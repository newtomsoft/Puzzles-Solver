import re

from Domain.Puzzles.Akari.AkariSolver import AkariSolver
from Domain.Puzzles.Aquarium.AquariumSolver import AquariumSolver
from Domain.Puzzles.Bimaru.BimaruSolver import BimaruSolver
from Domain.Puzzles.Binairo.BinairoSolver import BinairoSolver
from Domain.Puzzles.BinairoPlus.BinairoPlusSolver import BinairoPlusSolver
from Domain.Puzzles.Creek.CreekSolver import CreekSolver
from Domain.Puzzles.Dominosa.DominosaSolver import DominosaSolver
from Domain.Puzzles.Futoshiki.FutoshikiSolver import FutoshikiSolver
from Domain.Puzzles.GameSolver import GameSolver
from Domain.Puzzles.Hashi.HashiSolver import HashiSolver
from Domain.Puzzles.Heyawake.HeyawakeSolver import HeyawakeSolver
from Domain.Puzzles.Hitori.HitoriSolver import HitoriSolver
from Domain.Puzzles.Kakurasu.KakurasuSolver import KakurasuSolver
from Domain.Puzzles.Kakuro.KakuroSolver import KakuroSolver
from Domain.Puzzles.Kemaru.KemaruSolver import KemaruSolver
from Domain.Puzzles.KenKen.KenKenSolver import KenKenSolver
from Domain.Puzzles.Koburin.KoburinSolver import KoburinSolver
from Domain.Puzzles.Linesweeper.LinesweeperSolver import LinesweeperSolver
from Domain.Puzzles.Lits.LitsSolver import LitsSolver
from Domain.Puzzles.Masyu.MasyuSolver import MasyuSolver
from Domain.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver
from Domain.Puzzles.MinesweeperMosaic.MinesweeperMosaicSolver import MinesweeperMosaicSolver
from Domain.Puzzles.No4InARow.No4InARowSolver import No4InARowSolver
from Domain.Puzzles.Nonogram.NonogramSolver import NonogramSolver
from Domain.Puzzles.Norinori.NorinoriSolver import NorinoriSolver
from Domain.Puzzles.NumberChain.NumberChainSolver import NumberChainSolver
from Domain.Puzzles.NumberLink.NumberLinkSolver import NumberLinkSolver
from Domain.Puzzles.Nurikabe.NurikabeSolver import NurikabeSolver
from Domain.Puzzles.Pipes.PipesSolver import PipesSolver
from Domain.Puzzles.PipesWrap.PipesWrapSolver import PipesWrapSolver
from Domain.Puzzles.Purenrupu.PurenrupuSolver import PurenrupuSolver
from Domain.Puzzles.Renzoku.RenzokuSolver import RenzokuSolver
from Domain.Puzzles.Shikaku.ShikakuSolver import ShikakuSolver
from Domain.Puzzles.Shingoki.ShingokiSolver import ShingokiSolver
from Domain.Puzzles.Skyscrapers.SkyscrapersSolver import SkyscrapersSolver
from Domain.Puzzles.Snake.SnakeSolver import SnakeSolver
from Domain.Puzzles.StarBattle.StarBattleSolver import StarBattleSolver
from Domain.Puzzles.Stitches.StitchesSolver import StitchesSolver
from Domain.Puzzles.Str8ts.Str8tsSolver import Str8tsSolver
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
from GridPlayers.GridPuzzle.GridPuzzleCreekPlayer import GridPuzzleCreekPlayer
from GridPlayers.GridPuzzle.GridPuzzleHashiPlayer import GridPuzzleHashiPlayer
from GridPlayers.GridPuzzle.GridPuzzleKoburinPlayer import GridPuzzleKoburinPlayer
from GridPlayers.GridPuzzle.GridPuzzleLinesweeperPlayer import GridPuzzleLinesweeperPlayer
from GridPlayers.GridPuzzle.GridPuzzleNo4InARowPlayer import GridPuzzleNo4InARowPlayer
from GridPlayers.GridPuzzle.GridPuzzleNumberChainPlayer import GridPuzzleNumberChainPlayer
from GridPlayers.GridPuzzle.GridPuzzlePurenrupuPlayer import GridPuzzlePurenrupuPlayer
from GridPlayers.GridPuzzle.GridPuzzleShingokiPlayer import GridPuzzleShingokiPlayer
from GridPlayers.GridPuzzle.GridPuzzleSnakePlayer import GridPuzzleSnakePlayer
from GridPlayers.GridPuzzle.GridPuzzleStr8tsPlayer import GridPuzzleStr8tsPlayer
from GridPlayers.LinkedIn.QueensPlayer import QueensPlayer
from GridPlayers.LinkedIn.ZipPlayer import ZipPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronCalcudokuGridPlayer import PuzzleBaronCalcudokuPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronCampsitesGridPlayer import PuzzleBaronCampsitesPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronLaserGridsGridPlayer import PuzzleBaronLaserGridsPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronNumberLinksGridPlayer import PuzzleBaronNumberLinksPlayer
from GridPlayers.PuzzleBaron.PuzzleBaronStarBattleGridPlayer import PuzzleBaronStarBattlePlayer
from GridPlayers.PuzzleBaron.PuzzleBaronVectorsGridPlayer import PuzzleBaronVectorsPlayer
from GridPlayers.PuzzleMobiles.PuzzleAkariPlayer import PuzzleAkariPlayer
from GridPlayers.PuzzleMobiles.PuzzleAquariumPlayer import PuzzleAquariumPlayer
from GridPlayers.PuzzleMobiles.PuzzleBimaruPlayer import PuzzleBimaruPlayer
from GridPlayers.PuzzleMobiles.PuzzleBinairoPlayer import PuzzleBinairoPlayer
from GridPlayers.PuzzleMobiles.PuzzleDominosaPlayer import PuzzleDominosaPlayer
from GridPlayers.PuzzleMobiles.PuzzleFutoshikiPlayer import PuzzleFutoshikiPlayer
from GridPlayers.PuzzleMobiles.PuzzleHashiPlayer import PuzzleHashiPlayer
from GridPlayers.PuzzleMobiles.PuzzleHeyawakePlayer import PuzzleHeyawakePlayer
from GridPlayers.PuzzleMobiles.PuzzleHitoriPlayer import PuzzleHitoriPlayer
from GridPlayers.PuzzleMobiles.PuzzleKakurasuPlayer import PuzzleKakurasuPlayer
from GridPlayers.PuzzleMobiles.PuzzleKakuroPlayer import PuzzleKakuroPlayer
from GridPlayers.PuzzleMobiles.PuzzleLitsPlayer import PuzzleLitsPlayer
from GridPlayers.PuzzleMobiles.PuzzleMasyuPlayer import PuzzleMasyuPlayer
from GridPlayers.PuzzleMobiles.PuzzleMinesweeperMosaicPlayer import PuzzleMinesweeperMosaicPlayer
from GridPlayers.PuzzleMobiles.PuzzleMinesweeperPlayer import PuzzleMinesweeperPlayer
from GridPlayers.PuzzleMobiles.PuzzleNonogramsGrid import PuzzleNonogramsPlayer
from GridPlayers.PuzzleMobiles.PuzzleNorinoriPlayer import PuzzleNorinoriPlayer
from GridPlayers.PuzzleMobiles.PuzzleNurikabePlayer import PuzzleNurikabePlayer
from GridPlayers.PuzzleMobiles.PuzzlePipesPlayer import PuzzlePipesPlayer
from GridPlayers.PuzzleMobiles.PuzzleShikakuPlayer import PuzzleShikakuPlayer
from GridPlayers.PuzzleMobiles.PuzzleSkyscrapersPlayer import PuzzleSkyScrapersPlayer
from GridPlayers.PuzzleMobiles.PuzzleStarBattlePlayer import PuzzleStarBattlePlayer
from GridPlayers.PuzzleMobiles.PuzzleStitchesPlayer import PuzzleStitchesPlayer
from GridPlayers.PuzzleMobiles.PuzzleSudokuPlayer import PuzzleSudokuPlayer
from GridPlayers.PuzzleMobiles.PuzzleTapaPlayer import PuzzleTapaPlayer
from GridPlayers.PuzzleMobiles.PuzzleTentsPlayer import PuzzleTentsPlayer
from GridPlayers.PuzzleMobiles.PuzzleThermometersPlayer import PuzzleThermometersPlayer
from GridPlayers.VingtMinutes.VingtMinutesKemaruPlayer import VingtMinutesKemaruPlayer
from GridProviders.EscapeSudoku.EscapeSudokuProvider import EscapeSudokuGridProvider
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleCreekGridProvider import GridPuzzleCreekGridProvider
from GridProviders.GridPuzzle.GridPuzzleHashiGridProvider import GridPuzzleHashiGridProvider
from GridProviders.GridPuzzle.GridPuzzleKoburinGridProvider import GridPuzzleKoburinGridProvider
from GridProviders.GridPuzzle.GridPuzzleLinesweeperGridProvider import GridPuzzleLinesweeperGridProvider
from GridProviders.GridPuzzle.GridPuzzleNo4InARowGridProvider import GridPuzzleNo4InARowGridProvider
from GridProviders.GridPuzzle.GridPuzzleNumberChainGridProvider import GridPuzzleNumberChainGridProvider
from GridProviders.GridPuzzle.GridPuzzlePurenrupuGridProvider import GridPuzzlePurenrupuGridProvider
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
from GridProviders.VingtMinutes.VingtMinutesKemaruGridProvider import VingtMinutesKemaruGridProvider


class UrlPatternMatcher:
    def get_components_for_url(self, url: str) -> tuple[type[GameSolver], type[GridProvider], type[GridPlayer] | None]:
        if not url or url.strip() == "":
            raise ValueError("Please enter a valid URL")

        url_patterns = self.get_url_patterns()

        for pattern, components in url_patterns.items():
            if re.match(pattern, url):
                return components

        raise ValueError(f"No matching pattern found for URL: {url}")

    @staticmethod
    def get_url_patterns():
        return {
            r"https://.*\.puzzle-light-up\.com": (AkariSolver, PuzzleAkariGridProvider, PuzzleAkariPlayer),
            r"https://lasergrids\.puzzlebaron\.com/init2\.php": (AkariSolver, PuzzleBaronLaserGridsGridProvider, PuzzleBaronLaserGridsPlayer),
            r"https://.*\.puzzle-aquarium\.com": (AquariumSolver, PuzzleAquariumGridProvider, PuzzleAquariumPlayer),
            r"https://.*\.puzzle-battleships\.com": (BimaruSolver, PuzzleBimaruGridProvider, PuzzleBimaruPlayer),
            r"https://.*\.puzzle-binairo\.com/.*binairo-plus": (BinairoPlusSolver, PuzzleBinairoPlusGridProvider, PuzzleBinairoPlayer),  # same player as binairo
            r"https://.*\.puzzle-binairo\.com": (BinairoSolver, PuzzleBinairoGridProvider, PuzzleBinairoPlayer),
            r"https://.*gridpuzzle\.com/creek": (CreekSolver, GridPuzzleCreekGridProvider, GridPuzzleCreekPlayer),
            r"https://.*\.puzzle-dominosa\.com": (DominosaSolver, PuzzleDominosaGridProvider, PuzzleDominosaPlayer),
            r"https://.*\.puzzle-futoshiki\.com/.*renzoku": (RenzokuSolver, PuzzleRenzokuGridProvider, PuzzleFutoshikiPlayer),  # same player as futoshiki
            r"https://.*\.puzzle-futoshiki\.com": (FutoshikiSolver, PuzzleFutoshikiGridProvider, PuzzleFutoshikiPlayer),
            r"https://.*\.puzzle-bridges\.com": (HashiSolver, PuzzleHashiGridProvider, PuzzleHashiPlayer),
            r"https://.*gridpuzzle\.com/bridges": (HashiSolver, GridPuzzleHashiGridProvider, GridPuzzleHashiPlayer),
            r"https://.*\.puzzle-heyawake\.com": (HeyawakeSolver, PuzzleHeyawakeGridProvider, PuzzleHeyawakePlayer),
            r"https://.*\.puzzle-hitori\.com": (HitoriSolver, PuzzleHitoriGridProvider, PuzzleHitoriPlayer),
            r"https://.*\.puzzle-jigsaw-sudoku\.com": (JigsawSudokuSolver, PuzzleJigsawSudokuGridProvider, PuzzleSudokuPlayer),  # same player as sudoku
            r"https://.*\.puzzle-kakurasu\.com": (KakurasuSolver, PuzzleKakurasuGridProvider, PuzzleKakurasuPlayer),
            r"https://.*\.puzzle-kakuro\.com": (KakuroSolver, PuzzleKakuroGridProvider, PuzzleKakuroPlayer),
            r"https://www\.20minutes\.fr/services/jeux/kemaru": (KemaruSolver, VingtMinutesKemaruGridProvider, VingtMinutesKemaruPlayer),
            r"https://calcudoku\.puzzlebaron\.com/init2\.php": (KenKenSolver, PuzzleBaronCalcudokuGridProvider, PuzzleBaronCalcudokuPlayer),
            r"https://.*\.puzzle-killer-sudoku\.com": (KillerSudokuSolver, PuzzleKillerSudokuGridProvider, PuzzleSudokuPlayer),  # same player as Sudoku
            r"https://.*gridpuzzle\.com/koburin": (KoburinSolver, GridPuzzleKoburinGridProvider, GridPuzzleKoburinPlayer),
            r"https://.*gridpuzzle\.com/linesweeper":(LinesweeperSolver, GridPuzzleLinesweeperGridProvider, GridPuzzleLinesweeperPlayer),
            r"https://.*\.puzzle-lits\.com": (LitsSolver, PuzzleLitsGridProvider, PuzzleLitsPlayer),
            r"https://.*\.puzzle-masyu\.com": (MasyuSolver, PuzzleMasyuGridProvider, PuzzleMasyuPlayer),
            r"https://.*\.puzzle-minesweeper\.com/.*mosaic": (MinesweeperMosaicSolver, PuzzleMinesweeperMosaicGridProvider, PuzzleMinesweeperMosaicPlayer),
            r"https://.*\.puzzle-minesweeper\.com": (MinesweeperSolver, PuzzleMinesweeperMosaicGridProvider, PuzzleMinesweeperPlayer),
            r"https://.*\.puzzle-nonograms\.com": (NonogramSolver, PuzzleNonogramGridProvider, PuzzleNonogramsPlayer),
            r"https://.*\.puzzle-norinori\.com": (NorinoriSolver, PuzzleNorinoriGridProvider, PuzzleNorinoriPlayer),
            r"https://.*gridpuzzle\.com/no-four-in-row": (No4InARowSolver, GridPuzzleNo4InARowGridProvider, GridPuzzleNo4InARowPlayer),
            r"https://.*gridpuzzle\.com/number-chain": (NumberChainSolver, GridPuzzleNumberChainGridProvider, GridPuzzleNumberChainPlayer),
            r"https://numberlinks\.puzzlebaron\.com/init2\.php": (NumberLinkSolver, PuzzleBaronNumberLinksGridProvider, PuzzleBaronNumberLinksPlayer),
            r"https://.*\.puzzle-nurikabe\.com": (NurikabeSolver, PuzzleNurikabeGridProvider, PuzzleNurikabePlayer),
            r"https://.*\.puzzle-pipes\.com/\?size=\d{2,}": (PipesWrapSolver, PuzzlePipesGridProvider, PuzzlePipesPlayer),  # same player and same grid provider as pipes
            r"https://.*\.puzzle-pipes\.com": (PipesSolver, PuzzlePipesGridProvider, PuzzlePipesPlayer),
            r"https://.*gridpuzzle\.com/pure-loop": (PurenrupuSolver, GridPuzzlePurenrupuGridProvider, GridPuzzlePurenrupuPlayer),
            r"https://.*\.puzzle-shikaku\.com": (ShikakuSolver, PuzzleShikakuGridProvider, PuzzleShikakuPlayer),
            r"https://.*\.puzzle-shingoki\.com": (ShingokiSolver, PuzzleShingokiGridProvider, PuzzleMasyuPlayer),  # same player as masyu
            r"https://.*gridpuzzle\.com/traffic-lights": (ShingokiSolver, GridPuzzleShingokiGridProvider, GridPuzzleShingokiPlayer),
            r"https://.*\.puzzle-skyscrapers\.com": (SkyscrapersSolver, PuzzleSkyscrapersGridProvider, PuzzleSkyScrapersPlayer),
            r"https://.*gridpuzzle\.com/snake": (SnakeSolver, GridPuzzleSnakeGridProvider, GridPuzzleSnakePlayer),
            r"https://.*\.puzzle-star-battle\.com": (StarBattleSolver, PuzzleStarBattleGridProvider, PuzzleStarBattlePlayer),
            r"https://starbattle\.puzzlebaron\.com/init2\.php": (StarBattleSolver, PuzzleBaronStarBattleGridProvider, PuzzleBaronStarBattlePlayer),
            r"https://www\.linkedin\.com/games/queens": (StarBattleSolver, QueensGridProvider, QueensPlayer),
            r"https://.*\.puzzle-stitches\.com": (StitchesSolver, PuzzleStitchesGridProvider, PuzzleStitchesPlayer),
            r"https://.*gridpuzzle\.com/str8ts.": (Str8tsSolver, GridPuzzleStr8tsGridProvider, GridPuzzleStr8tsPlayer),
            r"https://.*\.puzzle-sudoku\.com": (SudokuSolver, PuzzleSudokuGridProvider, PuzzleSudokuPlayer),
            r"https://escape-sudoku.com/": (SudokuSolver, EscapeSudokuGridProvider, None),
            r"https://.*\.puzzle-loop\.com": (SurizaSolver, PuzzleSurizaGridProvider, PuzzleMasyuPlayer),  # same player as masyu
            r"https://playsumplete\.com/": (SumpleteSolver, PlaySumpleteGridProvider, None),
            r"https://.*\.puzzle-tapa\.com": (TapaSolver, PuzzleTapaGridProvider, PuzzleTapaPlayer),
            r"https://.*\.puzzle-galaxies\.com": (TentaiShowSolver, PuzzleTentaiShowGridProvider, None),
            r"https://.*\.puzzle-tents\.com": (TentsSolver, PuzzleTentsGridProvider, PuzzleTentsPlayer),
            r"https://campsites\.puzzlebaron\.com/init2\.php": (TentsSolver, PuzzleBaronCampsitesGridProvider, PuzzleBaronCampsitesPlayer),
            r"https://.*\.puzzle-thermometers\.com": (ThermometersSolver, PuzzleThermometersGridProvider, PuzzleThermometersPlayer),
            r"https://vectors\.puzzlebaron\.com/init2\.php": (VectorsSolver, PuzzleBaronVectorsGridProvider, PuzzleBaronVectorsPlayer),
            r"https://.*\.puzzle-yin-yang\.com": (YinYangSolver, PuzzleYinYangGridProvider, PuzzleBinairoPlayer),  # same player as binairo
            r"https://www\.linkedin\.com/games/zip": (ZipSolver, ZipGridProvider, ZipPlayer),
        }