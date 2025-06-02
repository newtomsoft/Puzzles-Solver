from time import sleep

from Domain.Board.Direction import Direction
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobilePlayer


class PuzzleDominosaGridPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell")
        unknown_coefficient = 1.25
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            box = cells.nth(index).bounding_box()
            if value == Direction._DOWN:
                page.mouse.move(box['x'] + box['width'] / 2, box['y'] + unknown_coefficient * box['height'])
                page.mouse.down()
                page.mouse.up()
            elif value == Direction._RIGHT:
                page.mouse.move(box['x'] + unknown_coefficient * box['width'], box['y'] + box['height'] / 2)
                page.mouse.down()
                page.mouse.up()
        sleep(2)
        self.submit_score(page)
        sleep(60)
