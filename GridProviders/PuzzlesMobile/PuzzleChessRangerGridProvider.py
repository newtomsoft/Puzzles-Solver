from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.ChessRanger.ChessRangerSolver import ChessRangerSolver
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleChessRangerGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.cell')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')

        if not cell_divs:
             raise ValueError("No cells found. Check selector.")

        # Determine dimensions logic (same as Kurodoko)
        rows_number = sum(1 for cell in cell_divs if 'left: 1px' in cell['style'])
        columns_number = sum(1 for cell in cell_divs if 'top: 1px' in cell['style'])
        cells_count = len(cell_divs)

        if columns_number == 0 or rows_number == 0:
            raise ValueError(f"Could not determine dimensions. Found {cells_count} cells.")

        # Filter hidden cells if any
        if columns_number * rows_number != cells_count:
             filtered_cells = [c for c in cell_divs if 'top:' in c['style'] and 'left:' in c['style']]
             if len(filtered_cells) != cells_count:
                 cell_divs = filtered_cells
                 rows_number = sum(1 for cell in cell_divs if 'left: 1px' in cell['style'])
                 columns_number = sum(1 for cell in cell_divs if 'top: 1px' in cell['style'])
                 cells_count = len(cell_divs)

             if columns_number * rows_number != cells_count:
                 raise ValueError(f"Grid parsing error: {rows_number}x{columns_number} != {cells_count}")

        # Parse pieces
        # Pieces are likely in class names or inner text.
        # Common pattern: class="cell piece-king" or inner span
        # If text is present, it might be unicode.

        # Mapping attempts
        piece_map = {
            'chess-king': 'K', 'king': 'K',
            'chess-queen': 'Q', 'queen': 'Q',
            'chess-rook': 'R', 'rook': 'R',
            'chess-bishop': 'B', 'bishop': 'B',
            'chess-knight': 'N', 'knight': 'N',
            'chess-pawn': 'P', 'pawn': 'P',
        }

        matrix = [[None for _ in range(columns_number)] for _ in range(rows_number)]

        for i, cell in enumerate(cell_divs):
            r = i // columns_number
            c = i % columns_number

            # Check classes
            classes = cell.get('class', [])
            piece = None

            # Check for piece classes on the cell itself or children
            # Sometimes piece is a child div
            piece_div = cell.find('div', class_=lambda x: x and ('piece' in x or 'chess' in x))

            target_classes = classes
            if piece_div:
                target_classes = piece_div.get('class', [])

            # Fallback: check all classes
            all_classes = list(classes)
            if piece_div:
                all_classes.extend(piece_div.get('class', []))

            for cls in all_classes:
                for key, val in piece_map.items():
                    if key in cls:
                        piece = val
                        break
                if piece:
                    break

            # Fallback: check unicode in text if no classes found
            if not piece:
                text = cell.get_text().strip()
                if text:
                    # TODO: Add unicode mapping if needed
                    pass

            matrix[r][c] = piece

        return Grid(matrix)
