import math
from playwright.async_api import BrowserContext
from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

class VuqqHitoriGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()

        await page.goto(url)

        # Wait for grid cells.
        await page.wait_for_selector('.grid__cell .number', timeout=10000)

        # Get all number elements
        cells_locator = page.locator('.grid__cell .number')
        count = await cells_locator.count()

        if count == 0:
             await page.wait_for_timeout(1000)
             count = await cells_locator.count()

        if count == 0:
            raise Exception("No grid cells found")

        # Determine size
        size = int(math.isqrt(count))
        if size * size != count:
            raise Exception(f"Grid is not square. Found {count} cells.")

        # Extract numbers
        numbers = []
        for i in range(count):
            text = await cells_locator.nth(i).inner_text()
            numbers.append(int(text))

        # Construct grid
        matrix = []
        for r in range(size):
            row = numbers[r*size : (r+1)*size]
            matrix.append(row)

        return Grid(matrix)
