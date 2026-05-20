import math
from bs4 import BeautifulSoup
from rebrowser_playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Bimaru.BimaruSolver import BimaruSolver
from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleBattleshipsGridProvider(PlaywrightGridProvider, GridPuzzleProvider):
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

        puzzle_main = soup.find(id='puzzle-main')
        if not puzzle_main:
            raise ValueError("No puzzle-main found in HTML")

        size = 0
        for cls in puzzle_main.get('class', []):
            if cls.startswith('ps'):
                try:
                    size = int(cls[2:])
                    break
                except ValueError:
                    pass

        if size == 0:
            cells_count = len(puzzle_main.find_all('div', class_='cell', recursive=False))
            size = int(math.sqrt(cells_count))

        rows_count = size
        cols_count = size

        cells = puzzle_main.find_all('div', class_='cell', recursive=False)
        if len(cells) != rows_count * cols_count:
            raise ValueError(f"Expected {rows_count * cols_count} cells but found {len(cells)}")

        matrix = [[-1 for _ in range(cols_count)] for _ in range(rows_count)]

        for i, cell in enumerate(cells):
            row = i // cols_count
            col = i % cols_count
            classes = cell.get('class', [])

            data_t = None
            for cls in classes:
                if cls.startswith('r_ship_'):
                    data_t = cls.replace('r_ship_', '')
                    break

            if data_t and data_t in self._type_mapping:
                matrix[row][col] = self._type_mapping[data_t]
            elif 'water_cell' in classes:
                matrix[row][col] = BimaruSolver.water
            else:
                matrix[row][col] = -1

        ship_cells = self._get_ship_cells(soup, rows_count, cols_count)
        ships_number_by_size = self._get_ships_number_by_size(soup)

        return Grid(matrix), ship_cells, ships_number_by_size

    @staticmethod
    def _get_ship_cells(soup: BeautifulSoup, rows_count: int, cols_count: int) -> dict[str, list[int]]:
        row_clues = []
        left_container = soup.find('div', class_='fl_txt')
        if left_container:
            row_divs = left_container.find_all('div', class_='fl_rows')
            if not row_divs:
                row_divs = left_container.find_all('div', class_='text-center')
            for div in row_divs:
                val = div.get('data-val')
                if val is not None:
                    row_clues.append(int(val))

        col_clues = []
        top_container = soup.find('div', class_='ft_txt')
        if top_container:
            col_divs = top_container.find_all('div', class_='ft_cells')
            if not col_divs:
                col_divs = top_container.find_all('div', class_='text-center')
            for div in col_divs:
                val = div.get('data-val')
                if val is not None:
                    col_clues.append(int(val))

        if not row_clues:
            row_container = soup.find('div', class_='fl_txt')
            if row_container:
                inner_divs = row_container.find_all('div')
                for div in inner_divs:
                    text = div.get_text(strip=True)
                    if text.isdigit():
                        row_clues.append(int(text))
                        if len(row_clues) == rows_count:
                            break

        if not col_clues:
            col_container = soup.find('div', class_='ft_txt')
            if col_container:
                inner_divs = col_container.find_all('div')
                for div in inner_divs:
                    text = div.get_text(strip=True)
                    if text.isdigit():
                        col_clues.append(int(text))
                        if len(col_clues) == cols_count:
                            break

        return {'row': row_clues, 'column': col_clues}

    @staticmethod
    def _get_ships_number_by_size(soup: BeautifulSoup) -> dict[int, int]:
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

        return ships_number_by_size
