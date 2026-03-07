import re
from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.Kazoku.KazokuSolver import KazokuSolver
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleKazokuGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, ar_string_list, ab_string_list, size = self._get_canvas_data_extended(html_page)

        numbers_matrix = [[None for _ in range(size)] for _ in range(size)]
        circles_matrix = [[None for _ in range(size)] for _ in range(size)]

        for i in range(len(pqq_string_list)):
            row = i // size
            col = i % size
            val = pqq_string_list[i]
            
            # val can contain multiple hints, e.g. "C?"
            if 'C' in val:
                circles_matrix[row][col] = KazokuSolver.Circle
            if '?' in val:
                numbers_matrix[row][col] = KazokuSolver.Unknown
            
            # Check for digits
            digit_match = re.search(r'\d+', val)
            if digit_match:
                numbers_matrix[row][col] = int(digit_match.group())
            # '.' means empty cell, but we've already initialized to None
            
        open_grid = Grid([[set() for _ in range(size)] for _ in range(size)])
        for i in range(len(ar_string_list)):
            row = i // size
            col = i % size
            position = Position(row, col)
            cell_border_right, cell_border_bottom = ar_string_list[i], ab_string_list[i]
            
            if row > 0 and ab_string_list[i - size] == '0':
                open_grid[position].add(Direction.up())
            if col > 0 and ar_string_list[i - 1] == '0':
                open_grid[position].add(Direction.left())
            if cell_border_right == '0':
                open_grid[position].add(Direction.right())
            if cell_border_bottom == '0':
                open_grid[position].add(Direction.down())

        return Grid(numbers_matrix), Grid(circles_matrix)
