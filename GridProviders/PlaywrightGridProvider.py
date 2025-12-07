import configparser
import logging
import os
import tkinter as tk
from abc import abstractmethod

from playwright.sync_api import BrowserContext, sync_playwright

from GridProviders.GridProvider import GridProvider


class PlaywrightGridProvider(GridProvider):
    def __init__(self):
        self.config_file_name = 'ScrapingGridProvider.ini'
        self.config_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.extensions_path = ''
        self.user_data_path = ''
        self.headless = True
        self.record_video = True
        self.email = ''
        self.password = ''
        self.config = self.get_config()
        self._read_config()

    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    @abstractmethod
    def scrap_grid(self, browser: BrowserContext, url):
        pass

    def get_config(self):
        config_generic_file_path = os.path.join(self.config_dir_path, self.config_file_name)
        if not os.path.exists(config_generic_file_path):
            raise FileNotFoundError(f"Configuration file not found: {config_generic_file_path}")

        config = configparser.ConfigParser()
        config_paths = [config_generic_file_path]

        config_file_name = f'{self.__class__.__name__}.ini'
        config_path = os.path.join(self.config_dir_path, config_file_name)
        if not os.path.exists(config_path):
            logging.info(f"Configuration file not found: {config_path}")

        config_paths.append(config_path)
        config.read(config_paths)
        return config

    def _read_config(self):
        self.headless = self.config['DEFAULT']['headless'] == 'True'
        self.force_headless_if_screen_too_small = self.config['DEFAULT']['force_headless_if_screen_too_small'] == 'True'
        self.record_video = os.environ.get('PLAYWRIGHT_RECORD_VIDEO', 'True') == 'True'
        self.user_data_path = os.path.join(self.config_dir_path, self.config['DEFAULT']['user_data_path'])
        extensions_path = self.config['DEFAULT']['extensions_path']
        extensions_paths = extensions_path.split(',')
        extensions_paths = [os.path.join(self.config_dir_path, x) for x in extensions_paths if x]
        self.extensions_path = ','.join([str(path) if os.path.exists(str(path)) else '' for path in extensions_paths])
        self.email = self.config['DEFAULT']['email']
        self.password = self.config['DEFAULT']['password']

    def with_playwright(self, callback, source):
        screen_width, screen_height = self.screen_size()
        window_width, window_height = 800, 1080
        if not self.headless and self.force_headless_if_screen_too_small and (screen_width < window_width or screen_height < window_height):
            self.headless = True
            print('Screen too small, using headless mode')

        playwright = sync_playwright().start()

        launch_args = {
            'user_data_dir': self.user_data_path,
            'viewport': {"width": window_width, "height": window_height},
            'headless': self.headless,
        }
        if self.record_video:
            launch_args['record_video_dir'] = "videos/"
            launch_args['record_video_size'] = {"width": window_width, "height": window_height}

        launch_args['args'] = [
            f'--disable-extensions-except={self.extensions_path}',
            f'--load-extension={self.extensions_path}',
            '--start-maximized'
        ]

        browser_context = playwright.chromium.launch_persistent_context(**launch_args)
        var = callback(browser_context, source)
        return var, browser_context

    @staticmethod
    def screen_size() -> tuple[int, int]:
        if "PUZZLE_SOLVER_GUI_MODE" in os.environ:
            return 1920, 1080

        try:
            root = tk.Tk()
            root.withdraw()
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            return width, height
        except Exception:
            return 800, 600
