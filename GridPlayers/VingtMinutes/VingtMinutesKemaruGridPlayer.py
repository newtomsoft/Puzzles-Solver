from time import sleep

from Board.Grid import Grid
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class VingtMinutesKemaruGridPlayer(PuzzlesMobileGridPlayer, PlaywrightGridPlayer):
    def play(self, grid_solution: Grid):
        page = self.browser.pages[0]
        cells = page.query_selector_all("g.grid-cell")
        for position, solution_value in grid_solution:
            index = position.r * grid_solution.columns_number + position.c
            cells[index].click()
            page.keyboard.press(str(solution_value))

        sleep(6)
