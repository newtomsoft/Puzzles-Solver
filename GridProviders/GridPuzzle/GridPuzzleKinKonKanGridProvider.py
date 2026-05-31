from rebrowser_playwright.async_api import BrowserContext
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

class GridPuzzleKinKonKanGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        
        # 1. Extraire les régions à partir des bordures des cellules
        opened_grid = self.make_opened_grid_extended(row_count, column_count, matrix_cells)
        regions_grid = RegionsGrid.from_opened_grid(opened_grid)
        
        # 2. Extraire les textes des indices par bord
        def get_raw_clues(side_letter, count):
            container = soup.find('div', class_=f'f{side_letter}_txt')
            result = [''] * count
            if container:
                clue_divs = container.find_all('div', recursive=True, class_='hbvr')
                for i, div in enumerate(clue_divs):
                    if i < count:
                        text = div.get('data-v', '').strip()
                        result[i] = text
            return result

        indices = {
            'top': get_raw_clues('t', column_count),
            'bottom': get_raw_clues('b', column_count),
            'left': get_raw_clues('l', row_count),
            'right': get_raw_clues('r', row_count)
        }
        
        return regions_grid, indices

    def make_opened_grid_extended(self, row_count, column_count, matrix_cells) -> Grid:
        from bs4.element import AttributeValueList
        from PuzzleSolver.Board.Direction import Direction
        
        # Initialisation : toutes les directions sont fermées par défaut
        opened_grid = Grid([[set() for _ in range(column_count)] for _ in range(row_count)])
        
        for i, cell in enumerate(matrix_cells):
            position = Position(*divmod(i, column_count))
            classes = cell.get('class', AttributeValueList([]))
            
            # Gestion des classes border_V_H (V=Vertical/Right, H=Horizontal/Bottom)
            # Une valeur de '0' signifie qu'il n'y a PAS de bordure (donc ouvert)
            is_right_open = True
            is_bottom_open = True
            
            for cls in classes:
                if cls.startswith('border_'):
                    parts = cls.split('_')
                    if len(parts) >= 3:
                        if parts[1] == '1': is_right_open = False
                        if parts[2] == '1': is_bottom_open = False
            
            if is_right_open and position.c < column_count - 1:
                opened_grid[position].add(Direction.right())
                opened_grid[Position(position.r, position.c + 1)].add(Direction.left())
            
            if is_bottom_open and position.r < row_count - 1:
                opened_grid[position].add(Direction.down())
                opened_grid[Position(position.r + 1, position.c)].add(Direction.up())

        return opened_grid
