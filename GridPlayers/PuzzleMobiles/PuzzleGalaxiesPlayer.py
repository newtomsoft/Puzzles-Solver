from time import sleep

from playwright.sync_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleGalaxiesPlayer(PuzzlesMobilePlayer):
    def __init__(self, browser: BrowserContext):
        super().__init__(browser)
        self._solution: Grid | None = None

    def play(self, solution):
        self._solution = solution
        page = self.browser.pages[0]
        cells = page.query_selector_all("div.loop-task-cell")
        different_neighbors_positions = solution.find_different_neighbors_positions()
        self._draw_regions(cells, page, different_neighbors_positions)

        self.submit_score(page)
        sleep(5)

    def _draw_regions(self, cells, page, pairs_positions: list[tuple[Position, Position]]):
        for position0, position1 in pairs_positions:
            index = position0.r * self._solution.columns_number + position0.c
            self._click(position0.direction_to(position1), page, cells[index])

    @staticmethod
    def _click(direction: Direction, page, cell):
        cell_width = cell.bounding_box()['width']
        cell_height = cell.bounding_box()['height']
        x0 = cell.bounding_box()['x']
        y0 = cell.bounding_box()['y']
        if direction == Direction.right():
            page.mouse.move(x0 + cell_width, y0 + cell_height / 2)
            page.mouse.down()
            page.mouse.up()
            return
        if direction == Direction.down():
            page.mouse.move(x0 + cell_width / 2, y0 + cell_height)
            page.mouse.down()
            page.mouse.up()
            return
        raise ValueError(f"unexpected direction: {direction}")