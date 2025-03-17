from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer
from Utils.Direction import Direction
from Utils.IslandsGrid import IslandGrid


class PuzzleShingokiGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution: IslandGrid, browser: BrowserContext):
        page = browser.pages[0]
        horizontals = page.locator(".loop-horizontal")
        verticals = page.locator(".loop-vertical")
        for island in solution.islands.values():
            index_horizontal = island.position.r * (solution.columns_number - 1) + island.position.c
            index_vertical = island.position.r * solution.columns_number + island.position.c
            if Direction.right() in island.direction_position_bridges:
                box = horizontals.nth(index_horizontal).bounding_box()
                page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                page.mouse.down()
                page.mouse.up()
            if Direction.down() in island.direction_position_bridges:
                box = verticals.nth(index_vertical).bounding_box()
                page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                page.mouse.down()
                page.mouse.up()
        cls.submit_score(page)
        sleep(60)

