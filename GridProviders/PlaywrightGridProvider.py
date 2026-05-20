import configparser
import logging
import os
import tkinter as tk
from abc import abstractmethod
from typing import Any, cast

from rebrowser_playwright.async_api import BrowserContext, async_playwright

from GridProviders.GridProvider import GridProvider


class PlaywrightGridProvider(GridProvider):
    def __init__(self):
        self.config_file_name = "ScrapingGridProvider.ini"
        self.config_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.extensions_path = ""
        self.user_data_path = ""
        self.headless = False
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
        self.headless = self.config["DEFAULT"]["headless"] == "True" or os.environ.get("CI", "false").lower() == "true"
        self.force_headless_if_screen_too_small = self.config["DEFAULT"]["force_headless_if_screen_too_small"] == "True"
        self.record_video = os.environ.get("PLAYWRIGHT_RECORD_VIDEO", "True") == "True"
        self.user_data_path = os.path.join(self.config_dir_path, self.config["DEFAULT"]["user_data_path"])
        extensions_path = self.config["DEFAULT"]["extensions_path"]
        extensions_paths = extensions_path.split(",")
        extensions_paths = [os.path.join(self.config_dir_path, x) for x in extensions_paths if x]
        self.extensions_path = ",".join([str(path) for path in extensions_paths if os.path.exists(str(path))])
        self.email = self.config["DEFAULT"]["email"]
        self.password = self.config["DEFAULT"]["password"]
        self.browser_type = self.config["DEFAULT"].get("browser", "chromium")

    async def with_playwright(self, callback, source) -> tuple[Any, BrowserContext, Any]:
        # Clean up potential stale LOCK files from crashed sessions
        user_data_dir = os.path.join(self.config_dir_path, self.config["DEFAULT"]["user_data_path"])
        lock_file = os.path.join(user_data_dir, "Default", "LOCK")
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
            except OSError:
                pass

        screen_width, screen_height = self.screen_size()
        window_width, window_height = 1920, 1080
        if not self.headless and self.force_headless_if_screen_too_small and (screen_width < window_width or screen_height < window_height):
            print(f"Warning: Screen size ({screen_width}x{screen_height}) is smaller than the requested window ({window_width}x{window_height}).")
            print("Continuing in headed mode anyway as requested.")

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

        playwright = await async_playwright().start()
        try:
            launch_args = {
                "user_data_dir": self.user_data_path,
                "viewport": {"width": window_width, "height": window_height},
                "headless": self.headless,
                "user_agent": user_agent,
            }
            if self.record_video:
                launch_args["record_video_dir"] = "videos/"
                launch_args["record_video_size"] = {"width": window_width, "height": window_height}

            if self.browser_type == "chromium":
                chromium_args = [
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--disable-features=IsolateOrigins,site-per-process",
                    "--disable-features=BlockInsecurePrivateNetworkRequests",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--password-store=basic",
                    "--lang=en-US,en",
                    "--start-maximized",
                    "--window-size=1920,1080",
                    "--window-position=0,0",
                    "--disable-background-networking",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-breakpad",
                    "--disable-client-side-phishing-detection",
                    "--disable-component-update",
                    "--disable-default-apps",
                    "--disable-hang-monitor",
                    "--disable-popup-blocking",
                    "--disable-prompt-on-repost",
                    "--disable-renderer-backgrounding",
                    "--force-color-profile=srgb",
                    "--metrics-recording-only",
                    "--safebrowsing-disable-auto-update",
                ]
                if self.headless:
                    chromium_args.append("--headless=new")
                if not self.headless and os.environ.get("WAYLAND_DISPLAY"):
                    chromium_args.append("--ozone-platform-hint=auto")
                if self.extensions_path:
                    chromium_args.append(f"--disable-extensions-except={self.extensions_path}")
                    chromium_args.append(f"--load-extension={self.extensions_path}")
                launch_args["args"] = cast(Any, chromium_args)
                browser_context = await playwright.chromium.launch_persistent_context(**launch_args)
            else:
                launch_args["args"] = cast(Any, [])
                browser_context = await playwright.firefox.launch_persistent_context(**launch_args)

            await browser_context.add_init_script("""
                window.__origGEC = document.getElementsByClassName.bind(document);
                delete window.__pwInitScripts;
                if (navigator.webdriver === true) {
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                        configurable: true
                    });
                }
            """)

            if self.browser_type == "chromium":
                try:
                    pages = browser_context.pages
                    target_page = pages[0] if pages else await browser_context.new_page()
                    cdp_session = await browser_context.new_cdp_session(target_page)
                    await cdp_session.send("Network.setUserAgentOverride", {
                        "userAgent": user_agent,
                        "userAgentMetadata": {
                            "brands": [
                                {"brand": "Chromium", "version": "130"},
                                {"brand": "Google Chrome", "version": "130"},
                                {"brand": "Not=A?Brand", "version": "99"}
                            ],
                            "fullVersionList": [
                                {"brand": "Chromium", "version": "130.0.6723.69"},
                                {"brand": "Google Chrome", "version": "130.0.6723.69"},
                                {"brand": "Not=A?Brand", "version": "99.0.0.0"}
                            ],
                            "platform": "Windows",
                            "platformVersion": "10.0",
                            "architecture": "x64",
                            "model": "",
                            "mobile": False
                        }
                    })
                    # Maximize window via CDP
                    try:
                        window_info = await cdp_session.send("Browser.getWindowForTarget")
                        await cdp_session.send("Browser.setWindowBounds", {
                            "windowId": window_info["windowId"],
                            "bounds": {"windowState": "maximized"}
                        })
                    except Exception:
                        pass
                except Exception:
                    pass

            browser_context.set_default_navigation_timeout(60000)

            var = await callback(browser_context, source)
            return var, browser_context, playwright
        except Exception:
            await playwright.stop()
            raise

    @staticmethod
    def has_display() -> bool:
        try:
            root = tk.Tk()
            root.withdraw()
            root.destroy()
            return True
        except Exception:
            return False

    @staticmethod
    def screen_size() -> tuple[int, int]:
        if "PUZZLE_SOLVER_GUI_MODE" in os.environ:
            return 1920, 1080

        if not PlaywrightGridProvider.has_display():
            return 0, 0

        try:
            root = tk.Tk()
            root.withdraw()
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            root.destroy()
            return width, height
        except Exception:
            return 0, 0
