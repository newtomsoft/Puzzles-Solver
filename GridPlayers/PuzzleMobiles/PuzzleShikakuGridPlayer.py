from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer
from Domain.Grid.Grid import Grid


class PuzzleShikakuGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution: Grid, browser: BrowserContext):
        page = browser.pages[0]
        cells = page.locator(".cell, .task-cell")

        regions_to_draw = [region for region in solution.get_regions().values() if len(region) >= 2]
        for region in regions_to_draw[:-1]:
            index_up_left = min(region, key=lambda p: p.r).r * solution.columns_number + min(region, key=lambda p: p.c).c
            bounding_box_up_left = cells.nth(index_up_left).bounding_box()
            index_down_right = max(region, key=lambda p: p.r).r * solution.columns_number + max(region, key=lambda p: p.c).c
            bounding_box_down_right = cells.nth(index_down_right).bounding_box()
            page.mouse.move(bounding_box_up_left['x'] + bounding_box_up_left['width'] / 2, bounding_box_up_left['y'] + bounding_box_up_left['height'] / 2)
            page.mouse.down()
            page.mouse.move(bounding_box_down_right['x'] + bounding_box_down_right['width'] / 2, bounding_box_down_right['y'] + bounding_box_down_right['height'] / 2)
            page.mouse.up()

        sleep(2)
        cls.submit_score(page)
        sleep(60)

