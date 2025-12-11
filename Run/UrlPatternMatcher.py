import Run.Games.AkariConfig
import Run.Games.AquariumConfig
import Run.Games.ArofuroConfig
import Run.Games.BalanceLoopConfig
import Run.Games.BimaruConfig
import Run.Games.BinairoConfig
import Run.Games.BinairoPlusConfig
import Run.Games.BinairoPlusConfig
import Run.Games.BorderBlockConfig
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
import Run.Games.KurodokoConfig
import Run.Games.KuroshiroConfig
import Run.Games.LinesweeperConfig
import Run.Games.LitsConfig
import Run.Games.LookAirConfig
import Run.Games.MasyuConfig
import Run.Games.MeadowsConfig
import Run.Games.MidLoopConfig
import Run.Games.MinesweeperConfig
import Run.Games.MinesweeperMosaicConfig
import Run.Games.MintonetteConfig
import Run.Games.MitiConfig
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
import Run.Games.ShakashakaConfig
import Run.Games.ShikakuConfig
import Run.Games.ShingokiConfig
import Run.Games.ShirokuroConfig
import Run.Games.SkyscrapersConfig
import Run.Games.SlantConfig
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

        Run.Games.AkariConfig.register()
        Run.Games.AquariumConfig.register()
        Run.Games.ArofuroConfig.register()
        Run.Games.BalanceLoopConfig.register()
        Run.Games.BimaruConfig.register()
        Run.Games.BinairoConfig.register()
        Run.Games.BinairoPlusConfig.register()
        Run.Games.BinairoPlusConfig.register()
        Run.Games.BorderBlockConfig.register()
        Run.Games.ChoconaConfig.register()
        Run.Games.CloudsConfig.register()
        Run.Games.CountryRoadConfig.register()
        Run.Games.CreekConfig.register()
        Run.Games.DominosaConfig.register()
        Run.Games.DoppelblockConfig.register()
        Run.Games.DosunFuwariConfig.register()
        Run.Games.DotchiLoopConfig.register()
        Run.Games.EverySecondTurnConfig.register()
        Run.Games.FobidoshiConfig.register()
        Run.Games.From1ToXConfig.register()
        Run.Games.FutoshikiConfig.register()
        Run.Games.GappyConfig.register()
        Run.Games.GeradewegConfig.register()
        Run.Games.GradesConfig.register()
        Run.Games.GrandTourConfig.register()
        Run.Games.GyokusekiConfig.register()
        Run.Games.HakoiriConfig.register()
        Run.Games.HashiConfig.register()
        Run.Games.HeyawakeConfig.register()
        Run.Games.HitoriConfig.register()
        Run.Games.JigsawSudokuConfig.register()
        Run.Games.KakurasuConfig.register()
        Run.Games.KakuroConfig.register()
        Run.Games.KakuteruAnpuConfig.register()
        Run.Games.KanjoConfig.register()
        Run.Games.KemaruConfig.register()
        Run.Games.KenKenConfig.register()
        Run.Games.KillerSudokuConfig.register()
        Run.Games.KoburinConfig.register()
        Run.Games.KonarupuConfig.register()
        Run.Games.KurodokoConfig.register()
        Run.Games.KuroshiroConfig.register()
        Run.Games.LinesweeperConfig.register()
        Run.Games.LitsConfig.register()
        Run.Games.LookAirConfig.register()
        Run.Games.MasyuConfig.register()
        Run.Games.MeadowsConfig.register()
        Run.Games.MidLoopConfig.register()
        Run.Games.MinesweeperConfig.register()
        Run.Games.MinesweeperMosaicConfig.register()
        Run.Games.MintonetteConfig.register()
        Run.Games.MitiConfig.register()
        Run.Games.MoonsunConfig.register()
        Run.Games.NanroConfig.register()
        Run.Games.NeighboursConfig.register()
        Run.Games.No4InARowConfig.register()
        Run.Games.NonogramConfig.register()
        Run.Games.NorinoriConfig.register()
        Run.Games.NumberChainConfig.register()
        Run.Games.NumberCrossConfig.register()
        Run.Games.NumberLinkConfig.register()
        Run.Games.NurikabeConfig.register()
        Run.Games.PipelinkConfig.register()
        Run.Games.PipesConfig.register()
        Run.Games.PipesWrapConfig.register()
        Run.Games.PurenrupuConfig.register()
        Run.Games.RegionalYajilinConfig.register()
        Run.Games.RenkatsuConfig.register()
        Run.Games.RenzokuConfig.register()
        Run.Games.RoundTripConfig.register()
        Run.Games.SeeThroughConfig.register()
        Run.Games.ShakashakaConfig.register()
        Run.Games.ShikakuConfig.register()
        Run.Games.ShirokuroConfig.register()
        Run.Games.ShingokiConfig.register()
        Run.Games.SkyscrapersConfig.register()
        Run.Games.SlantConfig.register()
        Run.Games.SnakeConfig.register()
        Run.Games.StarBattleConfig.register()
        Run.Games.StarsAndArrowsConfig.register()
        Run.Games.StitchesConfig.register()
        Run.Games.Str8tsConfig.register()
        Run.Games.SudokuConfig.register()
        Run.Games.SumpleteConfig.register()
        Run.Games.SurizaConfig.register()
        Run.Games.TapaConfig.register()
        Run.Games.TasukueaConfig.register()
        Run.Games.TatamibariConfig.register()
        Run.Games.TentaiShowConfig.register()
        Run.Games.TentsConfig.register()
        Run.Games.ThermometersConfig.register()
        Run.Games.TilePaintConfig.register()
        Run.Games.TrilogyConfig.register()
        Run.Games.VectorsConfig.register()
        Run.Games.WamazuConfig.register()
        Run.Games.YajikabeConfig.register()
        Run.Games.YajilinConfig.register()
        Run.Games.YinYangConfig.register()
        Run.Games.ZipConfig.register()

        cls._initialized = True

    @staticmethod
    def get_components_for_url(url: str) -> tuple[type[GameSolver], type[GridProvider], type[GridPlayer] | None]:
        if not url or url.strip() == "":
            raise ValueError("Please enter a valid URL")

        return GameRegistry.get_components_for_url(url)
