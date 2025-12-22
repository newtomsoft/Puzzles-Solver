import configparser
import logging
import os
import tkinter as tk
from abc import abstractmethod
from typing import Any, cast

from playwright.async_api import BrowserContext, async_playwright

from GridProviders.GridProvider import GridProvider


class PlaywrightGridProvider(GridProvider):
    def __init__(self):
        self.config_file_name = "ScrapingGridProvider.ini"
        self.config_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.extensions_path = ""
        self.user_data_path = ""
        self.headless = True
        self.force_headless_if_screen_too_small = True
        self.record_video = True
        self.email = ""
        self.password = ""
        self.browser_type = "chromium"
        self.config = self.get_config()
        self._read_config()

    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    @abstractmethod
    async def scrap_grid(self, browser: BrowserContext, url):
        pass

    def get_config(self):
        config_generic_file_path = os.path.join(self.config_dir_path, self.config_file_name)
        if not os.path.exists(config_generic_file_path):
            raise FileNotFoundError(f"Configuration file not found: {config_generic_file_path}")

        config = configparser.ConfigParser()
        config_paths = [config_generic_file_path]

        config_file_name = f"{self.__class__.__name__}.ini"
        config_path = os.path.join(self.config_dir_path, config_file_name)
        if not os.path.exists(config_path):
            logging.info(f"Configuration file not found: {config_path}")

        config_paths.append(config_path)
        config.read(config_paths)
        return config

    def _read_config(self):
        self.headless = self.config["DEFAULT"]["headless"] == "True"
        self.force_headless_if_screen_too_small = self.config["DEFAULT"]["force_headless_if_screen_too_small"] == "True"
        self.record_video = os.environ.get("PLAYWRIGHT_RECORD_VIDEO", "True") == "True"
        self.user_data_path = os.path.join(self.config_dir_path, self.config["DEFAULT"]["user_data_path"])
        extensions_path = self.config["DEFAULT"]["extensions_path"]
        extensions_paths = extensions_path.split(",")
        extensions_paths = [os.path.join(self.config_dir_path, x) for x in extensions_paths if x]
        self.extensions_path = ",".join([str(path) if os.path.exists(str(path)) else "" for path in extensions_paths])
        self.email = self.config["DEFAULT"]["email"]
        self.email = self.config["DEFAULT"]["email"]
        self.password = self.config["DEFAULT"]["password"]
        self.browser_type = self.config["DEFAULT"].get("browser", "chromium")

    async def with_playwright(self, callback, source) -> tuple[Any, BrowserContext, Any]:
        screen_width, screen_height = self.screen_size()
        window_width, window_height = 900, 1000
        if not self.headless and self.force_headless_if_screen_too_small and (screen_width < window_width or screen_height < window_height):
            self.headless = False
            print("Screen too small, using headless mode")

        playwright = await async_playwright().start()
        try:
            launch_args = {
                "user_data_dir": self.user_data_path,
                "viewport": {"width": window_width, "height": window_height},
                "headless": self.headless,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
            if self.record_video:
                launch_args["record_video_dir"] = "videos/"
                launch_args["record_video_size"] = {"width": window_width, "height": window_height}

            if self.browser_type == "chromium":
                chromium_args = [f"--disable-extensions-except={self.extensions_path}", f"--load-extension={self.extensions_path}", "--start-maximized"]
                launch_args["args"] = cast(Any, chromium_args)
                browser_context = await playwright.chromium.launch_persistent_context(**launch_args)
            else:
                launch_args["args"] = cast(Any, [])
                browser_context = await playwright.firefox.launch_persistent_context(**launch_args)

            browser_context.set_default_navigation_timeout(60000)

            var = await callback(browser_context, source)
            return var, browser_context, playwright
        except Exception:
            await playwright.stop()
            raise

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
