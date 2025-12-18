from abc import ABC
from typing import Any

from playwright.async_api import BrowserContext


class GridProvider(ABC):
    @staticmethod
    async def get_grid(source: str) -> tuple[Any, BrowserContext]:
        pass
