from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleMintonettePlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "mintonette"

    def play_game(self, page, solution):
        # TODO: Implement play logic, possibly using self._draw_loop if applicable
        pass
