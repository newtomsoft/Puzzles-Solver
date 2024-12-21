from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer
from Utils.Direction import Direction


class PuzzleDominosaGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        cells = page.locator(".cell")
        unknown_coefficient = 1.25
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            box = cells.nth(index).bounding_box()
            if value == Direction.DOWN:
                page.mouse.move(box['x'] + box['width'] / 2, box['y'] + unknown_coefficient * box['height'])
                page.mouse.down()
                page.mouse.up()
            elif value == Direction.RIGHT:
                page.mouse.move(box['x'] + unknown_coefficient * box['width'], box['y'] + box['height'] / 2)
                page.mouse.down()
                page.mouse.up()
        cls.submit_score(page)
        sleep(60)
