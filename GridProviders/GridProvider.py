from abc import ABC
from typing import Tuple, Any

from playwright.sync_api import BrowserContext


class GridProvider(ABC):
    @staticmethod
    def get_grid(source: str) -> Tuple[Any, BrowserContext]:
        pass
