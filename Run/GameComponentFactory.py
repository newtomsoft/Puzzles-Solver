from typing import Any

from Views.grid_player import GridPlayer
from Run.UrlPatternMatcher import UrlPatternMatcher


from Domain.Abstractions.i_puzzle_solver import IPuzzleSolver


class GameComponentFactory:
    def __init__(self):
        self._url_matcher = UrlPatternMatcher()
    
    def create_components_from_url(self, url: str) -> tuple[type[IPuzzleSolver], Any, GridPlayer | None]:
        game_class, grid_provider_class, player_class = self._url_matcher.get_components_for_url(url)
        grid_provider = grid_provider_class()
        print(f"getting grid...")
        game_data, browser_context = grid_provider.get_grid(url)
        game_player = player_class(browser_context) if player_class is not None else None
        return game_class, game_data, game_player