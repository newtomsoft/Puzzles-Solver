import re
from typing import Type, Tuple, Optional, Dict

from Domain.Puzzles.GameSolver import GameSolver
from GridPlayers.GridPlayer import GridPlayer
from GridProviders.GridProvider import GridProvider


class GameRegistry:
    _registry: Dict[str, Tuple[Type[GameSolver], Type[GridProvider], Optional[Type[GridPlayer]]]] = {}

    @classmethod
    def register_game(cls, url_pattern: str, grid_provider: Type[GridProvider], grid_player: Optional[Type[GridPlayer]] = None):
        """
        Decorator to register a game solver with its associated provider and player.
        Usage:
        @GameRegistry.register_game(r"https://example.com/sudoku", MyGridProvider, MyGridPlayer)
        class MySudokuSolver(GameSolver):
            ...
        """
        def decorator(solver_class: Type[GameSolver]):
            cls._registry[url_pattern] = (solver_class, grid_provider, grid_player)
            return solver_class
        return decorator

    @classmethod
    def get_components_for_url(cls, url: str) -> Tuple[Type[GameSolver], Type[GridProvider], Optional[Type[GridPlayer]]]:
        for pattern, components in cls._registry.items():
            if re.match(pattern, url):
                return components
        raise ValueError(f"No matching pattern found for URL: {url}")

    @classmethod
    def get_all_patterns(cls):
        return cls._registry
