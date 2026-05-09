import math

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Bimaru.BimaruSolver import BimaruSolver
from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleBattleshipsRetrogradeGridProvider(PlaywrightGridProvider, GridPuzzleProvider):
    _type_mapping = {
        '2': BimaruSolver.ship_single,
        '3': BimaruSolver.ship_middle_input,
        '4': BimaruSolver.ship_top,
        '5': BimaruSolver.ship_right,
        '6': BimaruSolver.ship_bottom,
        '7': BimaruSolver.ship_left,
    }

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup = BeautifulSoup(html_page, 'html.parser')
        cells = soup.find_all('div', class_='r_ship_cell')
        if not cells:
            raise ValueError("No r_ship_cell found in HTML")

        size = int(math.sqrt(len(cells)))
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                cell = cells[i * size + j]
                data_t = str(cell.get('data-t', '0'))
                row.append(self._type_mapping.get(data_t, -1))

            matrix.append(row)

        ships_number_by_size = {}
        ship_infos = soup.find_all('div', class_='ship_infos_num')
        for info in ship_infos:
            info_id = info.get('id', '')
            if not info_id.startswith('ship_num'):
                continue
            size_str = info_id.replace('ship_num', '')
            if size_str.isdigit():
                ship_size = int(size_str)
                count = int(info.get('data-num', '0'))
                if count > 0:
                    ships_number_by_size[ship_size] = count

        return Grid(matrix), ships_number_by_size
