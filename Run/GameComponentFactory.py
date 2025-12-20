from typing import Any

from Domain.Puzzles.GameSolver import GameSolver
from GridPlayers.Base.GridPlayer import GridPlayer
from Run.UrlPatternMatcher import UrlPatternMatcher


class GameComponentFactory:
    def __init__(self):
        self._url_matcher = UrlPatternMatcher()

    async def create_components_from_url(self, url: str) -> tuple[type[GameSolver], Any, GridPlayer | None, Any, Any]:
        game_class, grid_provider_class, player_class = self._url_matcher.get_components_for_url(url)
        grid_provider = grid_provider_class()
        print("getting grid...")
        game_data, browser_context, playwright = await grid_provider.get_grid(url)
        game_player = player_class(browser_context) if player_class is not None else None
        return game_class, game_data, game_player, browser_context, playwright
    
    @staticmethod
    def create_solver(solver_class: type[GameSolver], data_game: Any) -> GameSolver:
        if isinstance(data_game, tuple):
            grid = data_game[0]
            extra_data = data_game[1:]
            return solver_class(grid, *extra_data)

        return solver_class(data_game)
