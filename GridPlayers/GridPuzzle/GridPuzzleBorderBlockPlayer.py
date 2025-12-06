from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridPlayers.GridPuzzle.Base.GridPuzzleRegionBorderPlayer import GridPuzzleRegionBorderPlayer


class GridPuzzleBorderBlockPlayer(GridPuzzleRegionBorderPlayer):
    game_name = "border-block"
    board_margin = 8

    def __init__(self, browser: BrowserContext):
        super().__init__(browser)
        self._solution: Grid = Grid.empty()
