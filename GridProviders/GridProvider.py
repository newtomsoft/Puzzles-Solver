from abc import ABC
from typing import Any

from playwright.sync_api import BrowserContext


class GridProvider(ABC):
    @staticmethod
    def get_grid(source: str) -> tuple[Any, BrowserContext]:
        pass
