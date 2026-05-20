import math
import re
from bs4 import BeautifulSoup
from rebrowser_playwright.async_api import BrowserContext
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

class GridPuzzleHiroimonoGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url: str) -> Grid:
        html_page = await self.get_html(browser, url, '.g_cell')
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup = BeautifulSoup(html_page, 'html.parser')

        matrix_cells = soup.find_all('div', class_='g_cell')
        if not matrix_cells:
            raise ValueError("No cells found with class 'g_cell'")

        cells_count = len(matrix_cells)
        visual_size = int(math.sqrt(cells_count))
        print(f"Scraping Hiroimono: {cells_count} cells found, visual size: {visual_size}x{visual_size}")

        stones = []
        for i, cell in enumerate(matrix_cells):
            r = i // visual_size
            c = i % visual_size
            if self._has_stone(cell):
                stones.append((r, c))

        if not stones:
            # Créer une matrice vide de la taille détectée par précaution
            return Grid([['.' for _ in range(visual_size)] for _ in range(visual_size)])

        # Extraction des limites pour réduire la grille au minimum nécessaire
        min_r, max_r = min(s[0] for s in stones), max(s[0] for s in stones)
        min_c, max_c = min(s[1] for s in stones), max(s[1] for s in stones)

        reduced_rows = max_r - min_r + 1
        reduced_cols = max_c - min_c + 1
        reduced_matrix = [['.' for _ in range(reduced_cols)] for _ in range(reduced_rows)]

        for r, c in stones:
            reduced_matrix[r - min_r][c - min_c] = 'S'

        return Grid(reduced_matrix)

    @staticmethod
    def _has_stone(cell) -> bool:
        """Détermine si une cellule contient une pierre."""
        # Pour Hiroimono, les pierres sont dans les q_cell (enfants des g_cell)
        if cell.find(class_='q_cell'):
            return True
        
        # Fallback au cas où le sélecteur a déjà renvoyé les q_cell directement
        classes = cell.get('class', [])
        if 'q_cell' in classes:
            return True
            
        return False
