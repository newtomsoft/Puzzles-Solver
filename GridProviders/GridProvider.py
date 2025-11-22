from typing import Any

from playwright.sync_api import BrowserContext

from Domain.Abstractions.i_grid_provider import IGridProvider


class GridProvider(IGridProvider):
    def get_grid(self, url: str) -> tuple[Any, BrowserContext]:
        pass
