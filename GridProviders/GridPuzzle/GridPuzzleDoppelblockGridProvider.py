from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleDoppelblockGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            try:
                matrix[row][col] = int(cell.text)
            except ValueError:
                matrix[row][col] = None

        left_container = soup.find('div', class_='fl_txt')
        left = []
        if left_container:
            left_divs = left_container.find_all('div', class_='justify-content-around')
            for div in left_divs:
                text = div.get_text(strip=True)
                text = text.replace('\xa0', '').strip()
                try:
                    left.append(int(text))
                except (ValueError, AttributeError):
                    left.append(None)

        up_container = soup.find('div', class_='ft_txt')
        up = []
        if up_container:
            up_divs = up_container.find_all('div', class_='text-center')
            for div in up_divs:
                text = div.get_text(strip=True)
                try:
                    up.append(int(text))
                except (ValueError, AttributeError):
                    up.append(None)

        return Grid(matrix), left, up
