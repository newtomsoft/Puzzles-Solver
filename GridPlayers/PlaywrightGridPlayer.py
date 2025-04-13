import datetime
import os
from abc import ABC, abstractmethod

from moviepy import VideoFileClip
from playwright.async_api import BrowserContext, Mouse
from playwright.sync_api import ElementHandle

from Board.Grid import Grid
from Board.Position import Position


class PlaywrightGridPlayer(ABC):
    @classmethod
    @abstractmethod
    def play(cls, solution, browser: BrowserContext):
        pass

    @classmethod
    def mouse_move(cls, mouse: Mouse, solution: Grid, position: Position, cell_divs: list[ElementHandle]):
        index = solution.get_index_from_position(position)
        bounding_box = cell_divs[index].bounding_box()
        x = bounding_box['x'] + bounding_box['width'] / 2
        y = bounding_box['y'] + bounding_box['height'] / 2
        mouse.move(x, y)

    @classmethod
    def mouse_click(cls, mouse: Mouse, solution: Grid, position: Position, cells_divs: list[ElementHandle]):
        index = solution.get_index_from_position(position)
        bounding_box = cells_divs[index].bounding_box()
        x = bounding_box['x'] + bounding_box['width'] / 2
        y = bounding_box['y'] + bounding_box['height'] / 2
        mouse.click(x, y)

    @classmethod
    def mouse_down(cls, mouse):
        mouse.down()

    @classmethod
    def mouse_up(cls, mouse):
        mouse.up()

    @classmethod
    def move_start_down_move_end_up(cls, mouse: Mouse, solution: Grid, start_position: Position, end_position: Position, cell_divs: list[ElementHandle]):
        start_index = solution.get_index_from_position(start_position)
        start_bounding_box = cell_divs[start_index].bounding_box()
        start_x = start_bounding_box['x'] + start_bounding_box['width'] / 2
        start_y = start_bounding_box['y'] + start_bounding_box['height'] / 2

        end_index = solution.get_index_from_position(end_position)
        end_bounding_box = cell_divs[end_index].bounding_box()
        end_x = end_bounding_box['x'] + end_bounding_box['width'] / 2
        end_y = end_bounding_box['y'] + end_bounding_box['height'] / 2

        mouse.move(start_x, start_y)
        mouse.down()
        mouse.move(end_x, end_y, steps=int(end_position.distance(start_position)))
        mouse.up()

    @classmethod
    def crop_video(cls, input_video_path: str, x1: int, y1: int, x2: int, y2: int):
        clip = VideoFileClip(input_video_path, audio=False)
        cropped_clip = clip.cropped(x1=x1, y1=y1, x2=x2, y2=y2)
        date_yyyy_mm_dd = datetime.datetime.now().strftime('%Y-%m-%d')
        output_path = f'{input_video_path[:-5]}-{date_yyyy_mm_dd}.mp4'
        cropped_clip.write_videofile(output_path)
        os.remove(input_video_path)
