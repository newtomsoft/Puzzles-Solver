import datetime
import os
from abc import abstractmethod
from dataclasses import dataclass
from time import sleep
from typing import Protocol

from moviepy import VideoFileClip
from playwright.sync_api import BrowserContext, Mouse, Video
from playwright.sync_api import ElementHandle, Page

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.GridPlayer import GridPlayer


class VideoFile(Protocol):
    def path(self) -> str:
        ...


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rectangle:
    top_left: Point
    bottom_right: Point

    @property
    def x1(self) -> int:
        return self.top_left.x

    @property
    def y1(self) -> int:
        return self.top_left.y

    @property
    def x2(self) -> int:
        return self.bottom_right.x

    @property
    def y2(self) -> int:
        return self.bottom_right.y

    @property
    def width(self) -> int:
        return self.bottom_right.x - self.top_left.x

    @property
    def height(self) -> int:
        return self.bottom_right.y - self.top_left.y

    @classmethod
    def from_coordinates(cls, x1: int, y1: int, x2: int, y2: int) -> 'Rectangle':
        return cls(Point(x1, y1), Point(x2, y2))


class PlaywrightPlayer(GridPlayer):
    game_name = None

    def __init__(self, browser: BrowserContext):
        self.browser = browser

    @abstractmethod
    def play(self, solution):
        pass

    @classmethod
    def mouse_move(cls, mouse: Mouse, solution: Grid, position: Position, cell_divs: list[ElementHandle], steps=1):
        index = solution.get_index_from_position(position)
        bounding_box = cell_divs[index].bounding_box()
        x = bounding_box['x'] + bounding_box['width'] / 2
        y = bounding_box['y'] + bounding_box['height'] / 2
        mouse.move(x, y, steps=steps)

    @classmethod
    def mouse_click_on_position(cls, mouse: Mouse, solution: Grid, position: Position, cells_divs: list[ElementHandle]):
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
    def mouse_click(cls, page):
        page.mouse.down()
        page.mouse.up()

    @classmethod
    def drag_n_drop(cls, mouse: Mouse, solution: Grid, start_position: Position, end_position: Position, cell_divs: list[ElementHandle]):
        cls.mouse_move(mouse, solution, start_position, cell_divs)
        cls.mouse_down(mouse)
        cls.mouse_move(mouse, solution, end_position, cell_divs, steps=int(end_position.distance(start_position)))
        cls.mouse_up(mouse)

    def _get_canvas_data(self, columns_number, rows_number):
        page = self.browser.pages[0]
        bounded_box = page.locator("canvas").bounding_box()
        x0 = bounded_box['x']
        y0 = bounded_box['y']
        width = bounded_box['width']
        height = bounded_box['height']
        cell_width = width / columns_number
        cell_height = height / rows_number
        return cell_height, cell_width, page, x0, y0

    @classmethod
    def _get_data_video(cls, frame, selector, page: Page, x_offset: int, y_offset: int, width_offset: int, height_offset: int) -> tuple[Video, Rectangle]:
        game_board_wrapper = frame.wait_for_selector(selector)
        bounding_box = game_board_wrapper.bounding_box()
        x1 = int(bounding_box['x']) - x_offset
        y1 = int(bounding_box['y']) - y_offset
        x2 = int(bounding_box['width']) + x1 + x_offset + width_offset
        y2 = int(bounding_box['height']) + y1 + y_offset + height_offset
        rectangle = Rectangle(Point(x1, y1), Point(x2, y2))
        return page.video, rectangle

    @classmethod
    def _get_data_video_viewport(cls, page: Page) -> tuple[Video, Rectangle]:
        viewport_size = page.viewport_size
        x1 = 0
        y1 = 0
        x2 = viewport_size['width']
        y2 = viewport_size['height']
        rectangle = Rectangle(Point(x1, y1), Point(x2, y2))
        return page.video, rectangle

    @classmethod
    def _process_video(cls, video_file: VideoFile, rect: Rectangle, start_time: float = 0) -> str:
        video_path = video_file.path()
        cls._crop_video(video_path, cls.game_name, rect, start_time)
        return video_path

    @classmethod
    def _crop_video(cls, input_video_path: str, name: str, rect: Rectangle, start_time: float):
        video_name = os.path.basename(input_video_path)
        video_path = os.path.dirname(input_video_path)
        _, video_name_extension = os.path.splitext(video_name)
        clip = VideoFileClip(input_video_path, audio=False)
        clip = clip.subclipped(start_time=start_time)
        cropped_clip = clip.cropped(x1=rect.x1, y1=rect.y1, x2=rect.x2, y2=rect.y2)
        date_time_format = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_video_name = f'{name}_{date_time_format}{video_name_extension}'
        output_path = os.path.join(video_path, new_video_name)
        cropped_clip.write_videofile(
            output_path,
            codec='libvpx-vp9',
            fps=30,
            bitrate=None,
            preset='medium',
            threads=8,
            ffmpeg_params=['-crf', '36', '-b:v', '0']
        )
        clip.close()
        cropped_clip.close()
        os.remove(input_video_path)

    def close(self, delay_sec: int = 3):
        sleep(delay_sec)
        self.browser.close()
