from time import sleep

from Board.Grid import Grid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class VingtMinutesKemaruPlayer(PuzzlesMobilePlayer, PlaywrightPlayer):
    def play(self, grid_solution: Grid):
        page = self.browser.pages[0]
        cells = page.query_selector_all("g.grid-cell")
        for position, solution_value in grid_solution:
            index = position.r * grid_solution.columns_number + position.c
            cells[index].click()
            page.keyboard.press(str(solution_value))

        sleep(6)
