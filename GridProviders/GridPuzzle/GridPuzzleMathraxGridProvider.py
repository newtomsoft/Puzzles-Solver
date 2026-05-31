from bs4 import BeautifulSoup
from rebrowser_playwright.async_api import BrowserContext
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

class GridPuzzleMathraxGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0] if browser.pages else await browser.new_page()
        await page.goto(url)
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cells = soup.find_all('div', class_='g_cell')
        size = int(len(cells) ** 0.5)
        matrix = [[0 for _ in range(size)] for _ in range(size)]
        constraints = []
        import re
        
        for i, cell in enumerate(cells):
            r = i // size
            c = i % size
            
            is_readonly = cell.get('data-readonly') == '1'
            if is_readonly:
                val_div = cell.find('div', class_='cell-value')
                if val_div:
                    val_text = val_div.get_text(strip=True)
                    if val_text.isdigit():
                        matrix[r][c] = int(val_text)
            else:
                val_div = cell.find('div', class_='cell-value')
                if val_div:
                    val_text = val_div.get_text(strip=True)
                    if val_text.isdigit():
                        matrix[r][c] = int(val_text)
            
            tip = cell.find('div', class_='tips_q')
            if tip:
                text = tip.get_text(strip=True)
                if text:
                    if text == 'E':
                        constraints.append({'pos': (r, c), 'op': 'E'})
                    elif text == 'O':
                        constraints.append({'pos': (r, c), 'op': 'O'})
                    else:
                        text = text.replace('x', '*')
                        text = text.replace('÷', '/')
                        match = re.search(r'(\d+)([+\-*/])', text)
                        if match:
                            val = int(match.group(1))
                            op = match.group(2)
                            constraints.append({'pos': (r, c), 'op': op, 'val': val})
                        else:
                            match = re.search(r'([+\-*/])(\d+)', text)
                            if match:
                                op = match.group(1)
                                val = int(match.group(2))
                                constraints.append({'pos': (r, c), 'op': op, 'val': val})
        
        return Grid(matrix), constraints
