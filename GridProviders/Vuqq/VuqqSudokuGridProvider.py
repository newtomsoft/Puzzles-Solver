from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class VuqqSudokuGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()

        await page.goto(url)
        # await page.wait_for_load_state('networkidle')
        await page.wait_for_selector('.grid')
        await page.wait_for_selector('.grid__cell')

        # Wait for the grid to be populated (sometimes there's a delay)
        # Check if numbers are present or at least empty cells
        cells = await page.query_selector_all('.grid__cell')
        if len(cells) != 81:
             # Try forcing a wait
            await page.wait_for_timeout(1000)
            cells = await page.query_selector_all('.grid__cell')

        if len(cells) != 81:
            raise Exception(f"Expected 81 cells, found {len(cells)}")

        matrix = [[-1] * 9 for _ in range(9)]

        for i, cell in enumerate(cells):
            row = i // 9
            col = i % 9

            # The number is inside a span with class "number"
            number_span = await cell.query_selector('.number')
            if number_span:
                text = await number_span.inner_text()
                text = text.strip()
                if text.isdigit():
                    matrix[row][col] = int(text)
                else:
                    matrix[row][col] = -1
            else:
                matrix[row][col] = -1

        return Grid(matrix)
