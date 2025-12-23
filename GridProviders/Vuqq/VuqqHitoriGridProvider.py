import math
from playwright.async_api import BrowserContext
from Domain.Board.Grid import Grid
from GridProviders.Vuqq.Base.VuqqGridProvider import VuqqGridProvider


class VuqqHitoriGridProvider(VuqqGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url, ".grid")

        await page.wait_for_selector('.grid__cell .number', timeout=1000)

        cells_locator = page.locator('.grid__cell .number')
        count = await cells_locator.count()

        if count == 0:
             await page.wait_for_timeout(1000)
             count = await cells_locator.count()

        if count == 0:
            raise Exception("No grid cells found")

        size = int(math.isqrt(count))
        if size * size != count:
            raise Exception(f"Grid is not square. Found {count} cells.")

        numbers = []
        for i in range(count):
            text = await cells_locator.nth(i).inner_text()
            numbers.append(int(text))

        matrix = []
        for r in range(size):
            row = numbers[r*size : (r+1)*size]
            matrix.append(row)

        return Grid(matrix)
