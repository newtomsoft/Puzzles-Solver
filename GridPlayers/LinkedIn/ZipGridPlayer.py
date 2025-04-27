from time import sleep

from playwright.sync_api import BrowserContext

from Domain.Board.LinearPathGrid import LinearPathGrid
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class ZipGridPlayer(PlaywrightGridPlayer):
    @classmethod
    def play(cls, solution: LinearPathGrid, browser: BrowserContext):
        page = browser.pages[0]
        frame = page.frames[1]
        game_board = frame.wait_for_selector('.game-board')
        cells_divs = game_board.query_selector_all('div.trail-cell')

        video, rectangle = cls.get_data_video(frame, page, '.grid-board-wrapper', -12, -23, 22, 28)

        for position in solution.path:
            cls.mouse_click(page.mouse, solution, position, cells_divs)

        sleep(5)
        browser.close()
        cls.process_video(video, "zip", rectangle, 2)
