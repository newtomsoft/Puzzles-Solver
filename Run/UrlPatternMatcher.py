import Run.Games.AkariConfig
import Run.Games.AquariumConfig
import Run.Games.BalanceLoopConfig
import Run.Games.BimaruConfig
import Run.Games.BinairoConfig
import Run.Games.BinairoPlusConfig
import Run.Games.BinairoPlusConfig
import Run.Games.ChoconaConfig
import Run.Games.CloudsConfig
import Run.Games.CountryRoadConfig
import Run.Games.CreekConfig
import Run.Games.DominosaConfig
import Run.Games.DoppelblockConfig
import Run.Games.DosunFuwariConfig
import Run.Games.DotchiLoopConfig
import Run.Games.EverySecondTurnConfig
import Run.Games.FobidoshiConfig
import Run.Games.From1ToXConfig
import Run.Games.FutoshikiConfig
import Run.Games.GappyConfig
import Run.Games.GeradewegConfig
import Run.Games.GradesConfig
import Run.Games.GrandTourConfig
import Run.Games.GyokusekiConfig
import Run.Games.HakoiriConfig
import Run.Games.HashiConfig
import Run.Games.HeyawakeConfig
import Run.Games.HitoriConfig
import Run.Games.JigsawSudokuConfig
import Run.Games.KakurasuConfig
import Run.Games.KakuroConfig
import Run.Games.KakuteruAnpuConfig
import Run.Games.KanjoConfig
import Run.Games.KemaruConfig
import Run.Games.KenKenConfig
import Run.Games.KillerSudokuConfig
import Run.Games.KoburinConfig
import Run.Games.KonarupuConfig
import Run.Games.KuroshiroConfig
import Run.Games.LinesweeperConfig
import Run.Games.LitsConfig
import Run.Games.LookAirConfig
import Run.Games.MasyuConfig
import Run.Games.MeadowsConfig
import Run.Games.MidLoopConfig
import Run.Games.MinesweeperConfig
import Run.Games.MinesweeperMosaicConfig
import Run.Games.MoonsunConfig
import Run.Games.NanroConfig
import Run.Games.NeighboursConfig
import Run.Games.No4InARowConfig
import Run.Games.NonogramConfig
import Run.Games.NorinoriConfig
import Run.Games.NumberChainConfig
import Run.Games.NumberCrossConfig
import Run.Games.NumberLinkConfig
import Run.Games.NurikabeConfig
import Run.Games.PipelinkConfig
import Run.Games.PipesConfig
import Run.Games.PipesWrapConfig
import Run.Games.PurenrupuConfig
import Run.Games.RegionalYajilinConfig
import Run.Games.RenkatsuConfig
import Run.Games.RenzokuConfig
import Run.Games.RoundTripConfig
import Run.Games.SeeThroughConfig
import Run.Games.ShikakuConfig
import Run.Games.ShingokiConfig
import Run.Games.SkyscrapersConfig
import Run.Games.SnakeConfig
import Run.Games.StarBattleConfig
import Run.Games.StarsAndArrowsConfig
import Run.Games.StitchesConfig
import Run.Games.Str8tsConfig
import Run.Games.SudokuConfig
import Run.Games.SumpleteConfig
import Run.Games.SurizaConfig
import Run.Games.TapaConfig
import Run.Games.TasukueaConfig
import Run.Games.TatamibariConfig
import Run.Games.TentaiShowConfig
import Run.Games.TentsConfig
import Run.Games.ThermometersConfig
import Run.Games.TilePaintConfig
import Run.Games.TrilogyConfig
import Run.Games.VectorsConfig
import Run.Games.WamazuConfig
import Run.Games.YajikabeConfig
import Run.Games.YajilinConfig
import Run.Games.YinYangConfig
import Run.Games.ZipConfig
from Domain.Puzzles.GameSolver import GameSolver
from GridPlayers.GridPlayer import GridPlayer
from GridProviders.GridProvider import GridProvider
from Run.GameRegistry import GameRegistry


class UrlPatternMatcher:
    _initialized = False

    def __init__(self):
        self._initialize_registry()

    @classmethod
    def _initialize_registry(cls):
        if cls._initialized:
            return

        Run.Games.SudokuConfig.register_sudoku()
        Run.Games.ShingokiConfig.register_shingoki()
        Run.Games.AkariConfig.register_akari()
        Run.Games.AquariumConfig.register_aquarium()
        Run.Games.BalanceLoopConfig.register_balanceloop()
        Run.Games.BimaruConfig.register_bimaru()
        Run.Games.BinairoPlusConfig.register_binairoplus()
        Run.Games.BinairoConfig.register_binairo()
        Run.Games.ChoconaConfig.register_chocona()
        Run.Games.CloudsConfig.register_clouds()
        Run.Games.CountryRoadConfig.register_countryroad()
        Run.Games.CreekConfig.register_creek()
        Run.Games.DominosaConfig.register_dominosa()
        Run.Games.DoppelblockConfig.register_doppelblock()
        Run.Games.DosunFuwariConfig.register_dosunfuwari()
        Run.Games.DotchiLoopConfig.register_dotchiloop()
        Run.Games.EverySecondTurnConfig.register_everysecondturn()
        Run.Games.FobidoshiConfig.register_fobidoshi()
        Run.Games.From1ToXConfig.register_from1tox()
        Run.Games.RenzokuConfig.register_renzoku()
        Run.Games.FutoshikiConfig.register_futoshiki()
        Run.Games.GappyConfig.register_gappy()
        Run.Games.GeradewegConfig.register_geradeweg()
        Run.Games.GradesConfig.register_grades()
        Run.Games.GrandTourConfig.register_grandtour()
        Run.Games.GyokusekiConfig.register_gyokuseki()
        Run.Games.HakoiriConfig.register_hakoiri()
        Run.Games.HashiConfig.register_hashi()
        Run.Games.HeyawakeConfig.register_heyawake()
        Run.Games.HitoriConfig.register_hitori()
        Run.Games.JigsawSudokuConfig.register_jigsawsudoku()
        Run.Games.KakurasuConfig.register_kakurasu()
        Run.Games.KakuroConfig.register_kakuro()
        Run.Games.KakuteruAnpuConfig.register_kakuteruanpu()
        Run.Games.KanjoConfig.register_kanjo()
        Run.Games.KemaruConfig.register_kemaru()
        Run.Games.KenKenConfig.register_kenken()
        Run.Games.KillerSudokuConfig.register_killersudoku()
        Run.Games.KoburinConfig.register_koburin()
        Run.Games.KonarupuConfig.register_konarupu()
        Run.Games.KuroshiroConfig.register_kuroshiro()
        Run.Games.LinesweeperConfig.register_linesweeper()
        Run.Games.LitsConfig.register_lits()
        Run.Games.LookAirConfig.register_lookair()
        Run.Games.NanroConfig.register_nanro()
        Run.Games.MasyuConfig.register_masyu()
        Run.Games.MeadowsConfig.register_meadows()
        Run.Games.MidLoopConfig.register_midloop()
        Run.Games.MinesweeperMosaicConfig.register_minesweepermosaic()
        Run.Games.MinesweeperConfig.register_minesweeper()
        Run.Games.MoonsunConfig.register_moonsun()
        Run.Games.NeighboursConfig.register_neighbours()
        Run.Games.NonogramConfig.register_nonogram()
        Run.Games.NorinoriConfig.register_norinori()
        Run.Games.No4InARowConfig.register_no4inarow()
        Run.Games.NumberChainConfig.register_numberchain()
        Run.Games.NumberCrossConfig.register_numbercross()
        Run.Games.NumberLinkConfig.register_numberlink()
        Run.Games.NurikabeConfig.register_nurikabe()
        Run.Games.PipelinkConfig.register_pipelink()
        Run.Games.BinairoPlusConfig.register_binairoplus()
        Run.Games.PipesConfig.register_pipes()
        Run.Games.PipesWrapConfig.register_pipeswrap()
        Run.Games.PurenrupuConfig.register_purenrupu()
        Run.Games.RegionalYajilinConfig.register_regionalyajilin()
        Run.Games.RenkatsuConfig.register_renkatsu()
        Run.Games.RoundTripConfig.register_roundtrip()
        Run.Games.SeeThroughConfig.register_seethrough()
        Run.Games.ShikakuConfig.register_shikaku()
        Run.Games.SkyscrapersConfig.register_skyscrapers()
        Run.Games.SnakeConfig.register_snake()
        Run.Games.StarBattleConfig.register_starbattle()
        Run.Games.StarsAndArrowsConfig.register_starsandarrows()
        Run.Games.StitchesConfig.register_stitches()
        Run.Games.Str8tsConfig.register_str8ts()
        Run.Games.SumpleteConfig.register_sumplete()
        Run.Games.SurizaConfig.register_suriza()
        Run.Games.TapaConfig.register_tapa()
        Run.Games.TasukueaConfig.register_tasukuea()
        Run.Games.TatamibariConfig.register_tatamibari()
        Run.Games.TentaiShowConfig.register_tentaishow()
        Run.Games.TentsConfig.register_tents()
        Run.Games.ThermometersConfig.register_thermometers()
        Run.Games.TilePaintConfig.register_tilepaint()
        Run.Games.TrilogyConfig.register_trilogy()
        Run.Games.VectorsConfig.register_vectors()
        Run.Games.WamazuConfig.register_wamazu()
        Run.Games.YajikabeConfig.register_yajikabe()
        Run.Games.YajilinConfig.register_yajilin()
        Run.Games.YinYangConfig.register_yinyang()
        Run.Games.ZipConfig.register_zip()

        cls._initialized = True

    def get_components_for_url(self, url: str) -> tuple[type[GameSolver], type[GridProvider], type[GridPlayer] | None]:
        if not url or url.strip() == "":
            raise ValueError("Please enter a valid URL")

        return GameRegistry.get_components_for_url(url)

    @staticmethod
    def get_url_patterns():
        # Return the registry's patterns for backward compatibility if needed
        return GameRegistry.get_all_patterns()
