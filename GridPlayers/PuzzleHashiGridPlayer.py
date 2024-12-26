from time import sleep
from typing import Dict

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer
from Puzzles.Hashi.Island import Island
from Utils.Direction import Direction
from Utils.Position import Position


class PuzzleHachiGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution: Dict[Position, Island], browser: BrowserContext):
        page = browser.pages[0]
        cells = page.locator(".bridges-task-cell")
        for index, island in enumerate(solution.values()):
            box = cells.nth(index).bounding_box()
            for direction, (position, value) in island.direction_position_bridges.items():
                if direction == Direction.DOWN:
                    page.mouse.move(box['x'] + box['width'] // 2, box['y'] + box['height'] + 5)
                    for _ in range(value):
                        page.mouse.down()
                        page.mouse.up()
                elif direction == Direction.RIGHT:
                    page.mouse.move(box['x'] + box['width'] + 5, box['y'] + box['height'] // 2)
                    for _ in range(value):
                        page.mouse.down()
                        page.mouse.up()
        cls.submit_score(page)
        sleep(60)
