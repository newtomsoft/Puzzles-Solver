from time import sleep
from typing import Literal

from Domain.Board.Grid import Grid
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleKurodokoPlayer(PuzzlesMobilePlayer):
    def play(self, solution: Grid):
        page = self.browser.pages[0]
        url = page.url
        button: Literal['left', 'right'] = 'right' if 'puzzles-mobile' in url else 'left'

        cells = page.locator(".cell, .task-cell")
        for position in [position for position, value in solution if not value]:
            index = position.r * solution.columns_number + position.c
            cells.nth(index).click(button=button)

        self.submit_score(page)
        sleep(3)

