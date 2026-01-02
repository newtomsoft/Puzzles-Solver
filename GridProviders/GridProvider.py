from abc import ABC
from typing import Any

from playwright.async_api import BrowserContext


class GridProvider(ABC):
    @staticmethod
    async def get_grid(source: str) -> tuple[Any, BrowserContext, Any]:
        pass

    def get_grid_from_html(self, html: str, url: str) -> Any:
        raise NotImplementedError("This provider does not support extraction from HTML")
