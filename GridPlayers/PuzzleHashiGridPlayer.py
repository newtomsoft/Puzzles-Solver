from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer
from Utils.Direction import Direction
from Utils.IslandsGrid import IslandGrid


class PuzzleHashiGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution: IslandGrid, browser: BrowserContext):
        page = browser.pages[0]
        cells = page.locator(".bridges-task-cell")
        for index, island in enumerate(solution.islands.values()):
            box = cells.nth(index).bounding_box()
            for direction, (position, value) in island.direction_position_bridges.items():
                if direction == Direction.down():
                    page.mouse.move(box['x'] + box['width'] // 2, box['y'] + box['height'] + 5)
                    for _ in range(value):
                        page.mouse.down()
                        page.mouse.up()
                elif direction == Direction.right():
                    page.mouse.move(box['x'] + box['width'] + 5, box['y'] + box['height'] // 2)
                    for _ in range(value):
                        page.mouse.down()
                        page.mouse.up()
        cls.submit_score(page)
        sleep(60)
