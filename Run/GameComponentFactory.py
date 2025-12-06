from typing import Any

from Domain.Puzzles.GameSolver import GameSolver
from GridPlayers.GridPlayer import GridPlayer
from Run.PuzzleRunner import PuzzleRunner
from Run.UrlPatternMatcher import UrlPatternMatcher


class GameComponentFactory:
    def __init__(self):
        self._url_matcher = UrlPatternMatcher()
    
    def create_game(self, url: str) -> PuzzleRunner:
        game_class, grid_provider_class, player_class = self._url_matcher.get_components_for_url(url)
        grid_provider = grid_provider_class()
        print(f"getting grid...")
        game_data, browser_context = grid_provider.get_grid(url)

        if isinstance(game_data, tuple):
            grid = game_data[0]
            extra_data = game_data[1:]
            game_solver = game_class(grid, *extra_data)
        else:
            game_solver = game_class(game_data)

        game_player = player_class(browser_context) if player_class is not None else None

        return PuzzleRunner(game_solver, game_player)
