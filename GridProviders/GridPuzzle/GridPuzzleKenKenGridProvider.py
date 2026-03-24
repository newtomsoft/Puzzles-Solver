from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider


class GridPuzzleKenKenGridProvider(GridPuzzleTagProvider):
    async def scrap_grid(self, browser, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        grid = self.make_grid(column_count, matrix, matrix_cells)
        return grid
