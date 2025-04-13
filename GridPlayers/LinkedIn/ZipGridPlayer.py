from time import sleep

from playwright.sync_api import BrowserContext

from Board.LinearPathGrid import LinearPathGrid
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class ZipGridPlayer(PlaywrightGridPlayer):
    @classmethod
    def play(cls, solution: LinearPathGrid, browser: BrowserContext):
        page = browser.pages[0]
        frame = page.frames[1]
        game_board = frame.wait_for_selector('.game-board')
        cells_divs = game_board.query_selector_all('div.trail-cell')

        video, x1, x2, y1, y2 = cls.get_data_video(frame, page)

        for position in solution.path:
            cls.mouse_click(page.mouse, solution, position, cells_divs)

        sleep(6)
        browser.close()
        cls.process_video(video, x1, y1, x2, y2)

    @classmethod
    def get_data_video(cls, frame, page):
        game_board_wrapper = frame.wait_for_selector('.grid-board-wrapper')
        bounding_box = game_board_wrapper.bounding_box()
        x1 = int(bounding_box['x']) - 12
        y1 = int(bounding_box['y']) - 23
        x2 = int(bounding_box['width']) + x1 + 22
        y2 = int(bounding_box['height']) + y1 + 28
        video = page.video
        return video, x1, x2, y1, y2

    @classmethod
    def process_video(cls, video, x1, y1, x2, y2):
        input_video_path = video.path()
        cls.crop_video(input_video_path, x1, y1, x2, y2)
