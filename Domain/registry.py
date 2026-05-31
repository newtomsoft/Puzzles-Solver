"""Puzzle solver registry — maps puzzle names to solver classes."""

from Domain.Puzzles.Akari.AkariSolver import AkariSolver
from Domain.Puzzles.Aquarium.AquariumSolver import AquariumSolver
from Domain.Puzzles.Araf.ArafSolver import ArafSolver
from Domain.Puzzles.Arofuro.ArofuroSolver import ArofuroSolver
from Domain.Puzzles.ArrowWeb.ArrowWebSolver import ArrowWebSolver
from Domain.Puzzles.ArukoneNo2x2.ArukoneNo2x2Solver import ArukoneNo2x2Solver
from Domain.Puzzles.Ayeheya.AyeheyaSolver import AyeheyaSolver
from Domain.Puzzles.BalanceLoop.BalanceLoopSolver import BalanceLoopSolver
from Domain.Puzzles.Bimaru.BimaruSolver import BimaruSolver
from Domain.Puzzles.Binairo.BinairoSolver import BinairoSolver
from Domain.Puzzles.BinairoPlus.BinairoPlusSolver import BinairoPlusSolver
from Domain.Puzzles.BorderBlock.BorderBlockSolver import BorderBlockSolver
from Domain.Puzzles.Buraitoraito.BuraitoraitoSolver import BuraitoraitoSolver
from Domain.Puzzles.Chocona.ChoconaSolver import ChoconaSolver
from Domain.Puzzles.CirclesAndSquares.CirclesAndSquaresSolver import CirclesAndSquaresSolver
from Domain.Puzzles.Clouds.CloudsSolver import CloudsSolver
from Domain.Puzzles.Context.ContextSolver import ContextSolver
from Domain.Puzzles.CornerLoop.CornerLoopSolver import CornerLoopSolver
from Domain.Puzzles.Corral.CorralSolver import CorralSolver
from Domain.Puzzles.CountryRoad.CountryRoadSolver import CountryRoadSolver
from Domain.Puzzles.Creek.CreekSolver import CreekSolver
from Domain.Puzzles.Deddoanguru.DeddoanguruSolver import DeddoanguruSolver
from Domain.Puzzles.Detour.DetourSolver import DetourSolver
from Domain.Puzzles.Dominosa.DominosaSolver import DominosaSolver
from Domain.Puzzles.Doppelblock.DoppelblockSolver import DoppelblockSolver
from Domain.Puzzles.DosunFuwari.DosunFuwariSolver import DosunFuwariSolver
from Domain.Puzzles.DotchiLoop.DotchiLoopSolver import DotchiLoopSolver
from Domain.Puzzles.DoubleMinesweeper.DoubleMinesweeperSolver import DoubleMinesweeperSolver
from Domain.Puzzles.EverySecondTurn.EverySecondTurnSolver import EverySecondTurnSolver
from Domain.Puzzles.Factorism.FactorismSolver import FactorismSolver
from Domain.Puzzles.Fillomino.FillominoSolver import FillominoSolver
from Domain.Puzzles.FiveCells.FiveCellsSolver import FiveCellsSolver
from Domain.Puzzles.Fobidoshi.FobidoshiSolver import FobidoshiSolver
from Domain.Puzzles.Foseruzu.FoseruzuSolver import FoseruzuSolver
from Domain.Puzzles.From1ToX.From1ToXSolver import From1ToXSolver
from Domain.Puzzles.Fubuki.FubukiSolver import FubukiSolver
from Domain.Puzzles.Futoshiki.FutoshikiSolver import FutoshikiSolver
from Domain.Puzzles.Gappy.GappySolver import GappySolver
from Domain.Puzzles.Geradeweg.GeradewegSolver import GeradewegSolver
from Domain.Puzzles.Grades.GradesSolver import GradesSolver
from Domain.Puzzles.GrandTour.GrandTourSolver import GrandTourSolver
from Domain.Puzzles.Gyokuseki.GyokusekiSolver import GyokusekiSolver
from Domain.Puzzles.Hakoiri.HakoiriSolver import HakoiriSolver
from Domain.Puzzles.Hanare.HanareSolver import HanareSolver
from Domain.Puzzles.Hashi.HashiSolver import HashiSolver
from Domain.Puzzles.Heyablock.HeyablockSolver import HeyablockSolver
from Domain.Puzzles.Heyawake.HeyawakeSolver import HeyawakeSolver
from Domain.Puzzles.Hidoku.HidokuSolver import HidokuSolver
from Domain.Puzzles.Hiroimono.HiroimonoSolver import HiroimonoSolver
from Domain.Puzzles.Hitori.HitoriSolver import HitoriSolver
from Domain.Puzzles.Ichimaga.IchimagaSolver import IchimagaSolver
from Domain.Puzzles.Irasuto.IrasutoSolver import IrasutoSolver
from Domain.Puzzles.Island.IslandSolver import IslandSolver
from Domain.Puzzles.Kakurasu.KakurasuSolver import KakurasuSolver
from Domain.Puzzles.Kakuro.KakuroSolver import KakuroSolver
from Domain.Puzzles.KakuteruAnpu.KakuteruAnpuSolver import KakuteruAnpuSolver
from Domain.Puzzles.Kanjo.KanjoSolver import KanjoSolver
from Domain.Puzzles.Kazoku.KazokuSolver import KazokuSolver
from Domain.Puzzles.Kemaru.KemaruSolver import KemaruSolver
from Domain.Puzzles.KenKen.KenKenSolver import KenKenSolver
from Domain.Puzzles.KinKonKan.KinKonKanSolver import KinKonKanSolver
from Domain.Puzzles.Knossos.KnossosSolver import KnossosSolver
from Domain.Puzzles.Koburin.KoburinSolver import KoburinSolver
from Domain.Puzzles.KohiGyunyu.KohiGyunyuSolver import KohiGyunyuSolver
from Domain.Puzzles.Konarupu.KonarupuSolver import KonarupuSolver
from Domain.Puzzles.Kurodoko.KurodokoSolver import KurodokoSolver
from Domain.Puzzles.Kuroshiro.KuroshiroSolver import KuroshiroSolver
from Domain.Puzzles.Kuroshuto.KuroshutoSolver import KuroshutoSolver
from Domain.Puzzles.Kurotto.KurottoSolver import KurottoSolver
from Domain.Puzzles.Linesweeper.LinesweeperSolver import LinesweeperSolver
from Domain.Puzzles.Lits.LitsSolver import LitsSolver
from Domain.Puzzles.LookAir.LookAirSolver import LookAirSolver
from Domain.Puzzles.Map.MapSolver import MapSolver
from Domain.Puzzles.Marutaringu.MarutaringuSolver import MarutaringuSolver
from Domain.Puzzles.Masyu.MasyuSolver import MasyuSolver
from Domain.Puzzles.Mathrax.MathraxSolver import MathraxSolver
from Domain.Puzzles.Meadows.MeadowsSolver import MeadowsSolver
from Domain.Puzzles.MidLoop.MidLoopSolver import MidLoopSolver
from Domain.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver
from Domain.Puzzles.MinesweeperMosaic.MinesweeperMosaicSolver import MinesweeperMosaicSolver
from Domain.Puzzles.Mintonette.MintonetteSolver_or_tools import MintonetteSolver
from Domain.Puzzles.Mirukuti.MirukutiSolver import MirukutiSolver
from Domain.Puzzles.Mirukuti.MirukutiTeaseSolver import MirukutiTeaseSolver
from Domain.Puzzles.Miti.MitiSolver import MitiSolver
from Domain.Puzzles.Mobiriti.MobiritiSolver import MobiritiSolver
from Domain.Puzzles.Moonsun.MoonsunSolver import MoonsunSolver
from Domain.Puzzles.Nanro.NanroSolver import NanroSolver
from Domain.Puzzles.Neighbours.NeighboursSolver import NeighboursSolver
from Domain.Puzzles.No4InARow.No4InARowSolver import No4InARowSolver
from Domain.Puzzles.Nondango.NondangoSolver import NondangoSolver
from Domain.Puzzles.Nonogram.NonogramSolver import NonogramSolver
from Domain.Puzzles.Norinori.NorinoriSolver import NorinoriSolver
from Domain.Puzzles.NumberChain.NumberChainSolver import NumberChainSolver
from Domain.Puzzles.NumberCross.NumberCrossSolver import NumberCrossSolver
from Domain.Puzzles.NumberLink.NumberLinkSolver import NumberLinkSolver
from Domain.Puzzles.Nuribou.NuribouSolver import NuribouSolver
from Domain.Puzzles.Nurikabe.NurikabeSolver import NurikabeSolver
from Domain.Puzzles.Obitaru.ObitaruSolver import ObitaruSolver
from Domain.Puzzles.Pipelink.PipelinkSolver import PipelinkSolver
from Domain.Puzzles.Pipes.PipesSolver import PipesSolver
from Domain.Puzzles.PipesWrap.PipesWrapSolver import PipesWrapSolver
from Domain.Puzzles.Purenrupu.PurenrupuSolver import PurenrupuSolver
from Domain.Puzzles.Putteria.PutteriaSolver import PutteriaSolver
from Domain.Puzzles.RabbitsAndTrees.RabbitsAndTreesSolver import RabbitsAndTreesSolver
from Domain.Puzzles.RegionalYajilin.RegionalYajilinSolver import RegionalYajilinSolver
from Domain.Puzzles.Renkatsu.RenkatsuSolver import RenkatsuSolver
from Domain.Puzzles.Renzoku.RenzokuSolver import RenzokuSolver
from Domain.Puzzles.Rimotoejji.RimotoejjiSolver import RimotoejjiSolver
from Domain.Puzzles.RoundTrip.RoundTripSolver import RoundTripSolver
from Domain.Puzzles.Sashikazune.SashikazuneSolver import SashikazuneSolver
from Domain.Puzzles.SeeThrough.SeeThroughSolver import SeeThroughSolver
from Domain.Puzzles.Shakashaka.ShakashakaSolver import ShakashakaSolver
from Domain.Puzzles.SheepAndWolves.SheepAndWolvesSolver import SheepAndWolvesSolver
from Domain.Puzzles.Shikaku.ShikakuSolver import ShikakuSolver
from Domain.Puzzles.Shimaguni.ShimaguniSolver import ShimaguniSolver
from Domain.Puzzles.Shingoki.ShingokiSolver import ShingokiSolver
from Domain.Puzzles.Shirokuro.ShirokuroSolver import ShirokuroSolver
from Domain.Puzzles.Skyscrapers.SkyscrapersSolver import SkyscrapersSolver
from Domain.Puzzles.Slant.SlantSolver import SlantSolver
from Domain.Puzzles.Snake.SnakeSolver import SnakeSolver
from Domain.Puzzles.StarBattle.StarBattleSolver import StarBattleSolver
from Domain.Puzzles.StarsAndArrows.StarsAndArrowsSolver import StarsAndArrowsSolver
from Domain.Puzzles.Stitches.StitchesSolver import StitchesSolver
from Domain.Puzzles.Str8ts.Str8tsSolver import Str8tsSolver
from Domain.Puzzles.Sudoku.JigsawSudoku.JigsawSudokuSolver import JigsawSudokuSolver
from Domain.Puzzles.Sudoku.KillerSudoku.KillerSudokuSolver import KillerSudokuSolver
from Domain.Puzzles.Sudoku.Sudoku.SudokuSolver import SudokuSolver
from Domain.Puzzles.Summandum.SummandumSolver import SummandumSolver
from Domain.Puzzles.Sumplete.SumpleteSolver import SumpleteSolver
from Domain.Puzzles.Suriza.SurizaSolver import SurizaSolver
from Domain.Puzzles.Sutoreto.SutoretoSolver import SutoretoSolver
from Domain.Puzzles.Tapa.TapaSolver import TapaSolver
from Domain.Puzzles.Tasukuea.TasukueaSolver import TasukueaSolver
from Domain.Puzzles.Tatamibari.TatamibariSolver import TatamibariSolver
from Domain.Puzzles.TentaiShow.TentaiShowSolver import TentaiShowSolver
from Domain.Puzzles.Tents.TentsSolver import TentsSolver
from Domain.Puzzles.Thermometers.ThermometersSolver import ThermometersSolver
from Domain.Puzzles.TilePaint.TilePaintSolver import TilePaintSolver
from Domain.Puzzles.Toichika.ToichikaSolver import ToichikaSolver
from Domain.Puzzles.TraceNumbers.TraceNumbersSolver import TraceNumbersSolver
from Domain.Puzzles.Trilogy.TrilogySolver import TrilogySolver
from Domain.Puzzles.Usotatami.UsotatamiSolver import UsotatamiSolver
from Domain.Puzzles.Vectors.VectorsSolver import VectorsSolver
from Domain.Puzzles.Wamuzu.WamazuSolver import WamazuSolver
from Domain.Puzzles.Yajikabe.YajilkabeSolver import YajikabeSolver
from Domain.Puzzles.Yajilin.YajilinSolver import YajilinSolver
from Domain.Puzzles.YinYang.YinYangSolver import YinYangSolver
from Domain.Puzzles.Yonmasu.YonmasuSolver import YonmasuSolver
from Domain.Puzzles.Zip.ZipSolver import ZipSolver

SlitherlinkSolver = SurizaSolver

SOLVERS: dict[str, type] = {
    "akari": AkariSolver,
    "aquarium": AquariumSolver,
    "araf": ArafSolver,
    "arofuro": ArofuroSolver,
    "arrowweb": ArrowWebSolver,
    "arukoneno2x2": ArukoneNo2x2Solver,
    "ayeheya": AyeheyaSolver,
    "balanceloop": BalanceLoopSolver,
    "bimaru": BimaruSolver,
    "binairo": BinairoSolver,
    "binairoplus": BinairoPlusSolver,
    "borderblock": BorderBlockSolver,
    "buraitoraito": BuraitoraitoSolver,
    "chocona": ChoconaSolver,
    "circlesandsquares": CirclesAndSquaresSolver,
    "clouds": CloudsSolver,
    "context": ContextSolver,
    "cornerloop": CornerLoopSolver,
    "corral": CorralSolver,
    "countryroad": CountryRoadSolver,
    "creek": CreekSolver,
    "deddoanguru": DeddoanguruSolver,
    "detour": DetourSolver,
    "dominosa": DominosaSolver,
    "doppelblock": DoppelblockSolver,
    "dosunfuwari": DosunFuwariSolver,
    "dotchiloop": DotchiLoopSolver,
    "doubleminesweeper": DoubleMinesweeperSolver,
    "everysecondturn": EverySecondTurnSolver,
    "factorism": FactorismSolver,
    "fillomino": FillominoSolver,
    "fivecells": FiveCellsSolver,
    "fobidoshi": FobidoshiSolver,
    "foseruzu": FoseruzuSolver,
    "from1tox": From1ToXSolver,
    "fubuki": FubukiSolver,
    "futoshiki": FutoshikiSolver,
    "gappy": GappySolver,
    "geradeweg": GeradewegSolver,
    "grades": GradesSolver,
    "grandtour": GrandTourSolver,
    "gyokuseki": GyokusekiSolver,
    "hakoiri": HakoiriSolver,
    "hanare": HanareSolver,
    "hashi": HashiSolver,
    "heyablock": HeyablockSolver,
    "heyawake": HeyawakeSolver,
    "hidoku": HidokuSolver,
    "hiroimono": HiroimonoSolver,
    "hitori": HitoriSolver,
    "ichimaga": IchimagaSolver,
    "irasuto": IrasutoSolver,
    "island": IslandSolver,
    "jigsawsudoku": JigsawSudokuSolver,
    "kakurasu": KakurasuSolver,
    "kakuro": KakuroSolver,
    "kakuteruanpu": KakuteruAnpuSolver,
    "kanjo": KanjoSolver,
    "kazoku": KazokuSolver,
    "kemaru": KemaruSolver,
    "kenken": KenKenSolver,
    "killersudoku": KillerSudokuSolver,
    "kinkonkan": KinKonKanSolver,
    "knossos": KnossosSolver,
    "koburin": KoburinSolver,
    "kohigyunyu": KohiGyunyuSolver,
    "konarupu": KonarupuSolver,
    "kurodoko": KurodokoSolver,
    "kuroshiro": KuroshiroSolver,
    "kuroshuto": KuroshutoSolver,
    "kurotto": KurottoSolver,
    "linesweeper": LinesweeperSolver,
    "lits": LitsSolver,
    "lookair": LookAirSolver,
    "map": MapSolver,
    "marutaringu": MarutaringuSolver,
    "masyu": MasyuSolver,
    "mathrax": MathraxSolver,
    "meadows": MeadowsSolver,
    "midloop": MidLoopSolver,
    "minesweeper": MinesweeperSolver,
    "minesweepermosaic": MinesweeperMosaicSolver,
    "mintonette": MintonetteSolver,
    "mirukuti": MirukutiSolver,
    "mirukutitease": MirukutiTeaseSolver,
    "miti": MitiSolver,
    "mobiriti": MobiritiSolver,
    "moonsun": MoonsunSolver,
    "nanro": NanroSolver,
    "neighbours": NeighboursSolver,
    "no4inarow": No4InARowSolver,
    "nondango": NondangoSolver,
    "nonogram": NonogramSolver,
    "norinori": NorinoriSolver,
    "numberchain": NumberChainSolver,
    "numbercross": NumberCrossSolver,
    "numberlink": NumberLinkSolver,
    "nuribou": NuribouSolver,
    "nurikabe": NurikabeSolver,
    "obitaru": ObitaruSolver,
    "pipelink": PipelinkSolver,
    "pipes": PipesSolver,
    "pipeswrap": PipesWrapSolver,
    "purenrupu": PurenrupuSolver,
    "putteria": PutteriaSolver,
    "rabbitsandtrees": RabbitsAndTreesSolver,
    "regionalyajilin": RegionalYajilinSolver,
    "renkatsu": RenkatsuSolver,
    "renzoku": RenzokuSolver,
    "rimotoejji": RimotoejjiSolver,
    "roundtrip": RoundTripSolver,
    "sashikazune": SashikazuneSolver,
    "seethrough": SeeThroughSolver,
    "shakashaka": ShakashakaSolver,
    "sheepandwolves": SheepAndWolvesSolver,
    "shikaku": ShikakuSolver,
    "shimaguni": ShimaguniSolver,
    "shingoki": ShingokiSolver,
    "shirokuro": ShirokuroSolver,
    "skyscrapers": SkyscrapersSolver,
    "slant": SlantSolver,
    "slitherlink": SlitherlinkSolver,
    "snake": SnakeSolver,
    "starbattle": StarBattleSolver,
    "starsandarrows": StarsAndArrowsSolver,
    "stitches": StitchesSolver,
    "str8ts": Str8tsSolver,
    "sudoku": SudokuSolver,
    "summandum": SummandumSolver,
    "sumplete": SumpleteSolver,
    "suriza": SurizaSolver,
    "sutoreto": SutoretoSolver,
    "tapa": TapaSolver,
    "tasukuea": TasukueaSolver,
    "tatamibari": TatamibariSolver,
    "tentaishow": TentaiShowSolver,
    "tents": TentsSolver,
    "thermometers": ThermometersSolver,
    "tilepaint": TilePaintSolver,
    "toichika": ToichikaSolver,
    "tracenumbers": TraceNumbersSolver,
    "trilogy": TrilogySolver,
    "usotatami": UsotatamiSolver,
    "vectors": VectorsSolver,
    "wamazu": WamazuSolver,
    "yajilkabe": YajikabeSolver,
    "yajilin": YajilinSolver,
    "yinyang": YinYangSolver,
    "yonmasu": YonmasuSolver,
    "zip": ZipSolver,
}


def solve(puzzle_name: str, data, **kwargs):
    """Solve a puzzle by name.

    Args:
        puzzle_name: Lowercase puzzle name (e.g. "akari", "sudoku", "hashi").
        data: Data to pass to the solver constructor (Grid, dict, etc.).
        **kwargs: Additional arguments forwarded to the solver constructor.

    Returns:
        The puzzle solution (typically a Grid).
    """
    solver_class = SOLVERS[puzzle_name]
    solver = solver_class(data, **kwargs)
    return solver.get_solution()


def list_puzzles() -> list[str]:
    """Return sorted list of available puzzle names."""
    return sorted(SOLVERS.keys())
