import datetime
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from moviepy import VideoFileClip
from playwright.async_api import BrowserContext, Mouse
from playwright.sync_api import ElementHandle

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


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
    def get_data_video(cls, frame, page, selector, x_offset: int, y_offset: int, width_offset: int, height_offset: int) -> tuple[VideoFile, Rectangle]:
        game_board_wrapper = frame.wait_for_selector(selector)
        bounding_box = game_board_wrapper.bounding_box()
        x1 = int(bounding_box['x']) + x_offset
        y1 = int(bounding_box['y']) + y_offset
        x2 = int(bounding_box['width']) + x1 + width_offset
        y2 = int(bounding_box['height']) + y1 + height_offset
        rectangle = Rectangle(Point(x1, y1), Point(x2, y2))
        return page.video, rectangle

    @classmethod
    def process_video(cls, video_file: VideoFile, name: str, rect: Rectangle, start_time: int = 0) -> str:
        video_path = video_file.path()
        cls.crop_video(video_path, name, rect, start_time)
        return video_path

    @classmethod
    def crop_video(cls, input_video_path: str, name: str, rect: Rectangle, start_time: int):
        video_name = os.path.basename(input_video_path)
        video_path = os.path.dirname(input_video_path)
        video_name_without_extension, video_name_extension = os.path.splitext(video_name)
        clip = VideoFileClip(input_video_path, audio=False)
        clip = clip.subclipped(start_time=start_time)
        cropped_clip = clip.cropped(x1=rect.x1, y1=rect.y1, x2=rect.x2, y2=rect.y2)
        date_time_format = datetime.datetime.now().strftime('%H-%M-%S_%Y-%m-%d')
        new_video_name = f'{name}_{date_time_format}{video_name_extension}'
        output_path = os.path.join(video_path, new_video_name)
        cropped_clip.write_videofile(output_path)
        os.remove(input_video_path)
