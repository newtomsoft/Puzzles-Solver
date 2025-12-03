import re
from typing import Optional

from Domain.Puzzles.GameSolver import GameSolver
from GridPlayers.GridPlayer import GridPlayer
from GridProviders.GridProvider import GridProvider


class GameRegistry:
    _registry: dict[str, tuple[type[GameSolver], type[GridProvider], type[GridPlayer] | None]] = {}

    @classmethod
    def register(cls, url_pattern: str, grid_provider: type[GridProvider], grid_player: type[GridPlayer] | None = None):
        def decorator(solver_class: type[GameSolver]):
            cls._registry[url_pattern] = (solver_class, grid_provider, grid_player)
            return solver_class
        return decorator

    @classmethod
    def get_components_for_url(cls, url: str) -> tuple[type[GameSolver], type[GridProvider], Optional[type[GridPlayer]]]:
        for pattern, components in cls._registry.items():
            if re.match(pattern, url):
                return components
        raise ValueError(f"No matching pattern found for URL: {url}")

    @classmethod
    def get_all_patterns(cls):
        return cls._registry
