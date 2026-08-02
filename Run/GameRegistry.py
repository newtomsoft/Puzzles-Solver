import re
from typing import Optional

from PuzzleSolver.Puzzles.GameSolver import GameSolver
from GridPlayers.Base.GridPlayer import GridPlayer
from GridProviders.GridProvider import GridProvider


class GameRegistry:
    _registry: dict[str, tuple[type[GameSolver], type[GridProvider], type[GridPlayer] | None]] = {}
    _PZV_JP_URL_RE = re.compile(r"^https?://pzv\.jp/(?:p\.html|p)(\?.*)?$")

    @classmethod
    def register(cls, url_pattern: str, grid_provider: type[GridProvider], grid_player: type[GridPlayer] | None = None):
        def decorator(solver_class: type[GameSolver]):
            cls._registry[url_pattern] = (solver_class, grid_provider, grid_player)
            return solver_class
        return decorator

    @staticmethod
    def normalize_url(url: str) -> str:
        """Rewrite puzz.link aliases (e.g. pzv.jp) to the canonical https://puzz.link form."""
        return GameRegistry._PZV_JP_URL_RE.sub(r"https://puzz.link/p\1", url)

    @classmethod
    def get_components_for_url(cls, url: str) -> tuple[type[GameSolver], type[GridProvider], Optional[type[GridPlayer]]]:
        url = cls.normalize_url(url.strip())
        for pattern, components in cls._registry.items():
            if re.match(pattern, url):
                return components
        raise ValueError(f"No matching pattern found for URL: {url}")

    @classmethod
    def get_all_patterns(cls):
        return cls._registry
