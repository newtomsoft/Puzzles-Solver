from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.Vuqq.Base.VuqqGridProvider import VuqqGridProvider


class VuqqSudokuGridProvider(VuqqGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url, ".grid__cell")
        cells = await page.query_selector_all('.grid__cell')
        if len(cells) != 81:
            await page.wait_for_timeout(1000)
            cells = await page.query_selector_all('.grid__cell')

        if len(cells) != 81:
            raise Exception(f"Expected 81 cells, found {len(cells)}")

        matrix = [[-1] * 9 for _ in range(9)]

        for i, cell in enumerate(cells):
            row = i // 9
            col = i % 9

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
