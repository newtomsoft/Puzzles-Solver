import re
from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleKenKenGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    def _get_borders(self, classes):
        borders = set()
        for cls in classes:
            if cls.startswith('border_'):
                # border_X_Y: X is RIGHT, Y is BOTTOM
                parts = cls.split('_')
                if len(parts) == 3:
                    if parts[1] == '1':
                        borders.add(Direction.right())
                    if parts[2] == '1':
                        borders.add(Direction.down())
        return borders

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        soup, row_count, column_count, _, matrix_cells = self._get_grid_data(html_page)

        # On identifie les régions basées sur les frontières
        # Sur gridpuzzle.com, les classes border_X_Y indiquent si les bordures DROITE (X) et BAS (Y) sont fermées (1).
        
        # On construit un graphe d'adjacence : quelles cellules sont dans la même région
        adj = {Position(r, c): set() for r in range(row_count) for c in range(column_count)}
        
        for i, cell in enumerate(matrix_cells):
            r, c = divmod(i, column_count)
            pos = Position(r, c)
            classes = cell.get('class', [])
            borders = self._get_borders(classes)
            
            # Si pas de bordure à droite, on est dans la même région que le voisin de droite
            if Direction.right() not in borders and c < column_count - 1:
                right_pos = pos.right
                adj[pos].add(right_pos)
                adj[right_pos].add(pos)
                
            # Si pas de bordure en bas, on est dans la même région que le voisin du bas
            if Direction.down() not in borders and r < row_count - 1:
                down_pos = pos.down
                adj[pos].add(down_pos)
                adj[down_pos].add(pos)

        regions = []
        visited = set()
        for r in range(row_count):
            for c in range(column_count):
                pos = Position(r, c)
                if pos not in visited:
                    region = []
                    stack = [pos]
                    visited.add(pos)
                    while stack:
                        current = stack.pop()
                        region.append(current)
                        for neighbor in adj[current]:
                            if neighbor not in visited:
                                visited.add(neighbor)
                                stack.append(neighbor)
                    regions.append(region)

        # On extrait les opérations
        # Sur gridpuzzles.com, l'indice de l'opération est souvent dans une div 'tips_q' 
        # ou directement dans la cellule en haut à gauche de la région.
        regions_operators_results = []
        
        # On crée un mapping position -> region
        pos_to_region = {}
        for region in regions:
            for pos in region:
                pos_to_region[pos] = region

        # Parcourir les cellules pour trouver les indices (tip_num ou tips_q)
        for i, cell in enumerate(matrix_cells):
            r, c = divmod(i, column_count)
            pos = Position(r, c)
            tip = cell.find('div', class_=['tip_num', 'tips_q'])
            if tip:
                text = tip.get_text(strip=True)
                if text:
                    # Format attendu : "12x", "7+", "3-", "2÷", "3/" ou juste "5"
                    # On nettoie et on standardise
                    text = text.replace('x', '*').replace('÷', '/').replace(':', '/')
                    match = re.match(r'^(\d+)([+\-*/]?)$', text)
                    if not match:
                        # Parfois l'opérateur est devant : "/3"
                        match = re.match(r'^([+\-*/]?)(\d+)$', text)
                        if match:
                            operator = match.group(1)
                            result = int(match.group(2))
                        else:
                            continue
                    else:
                        result = int(match.group(1))
                        operator = match.group(2)
                    
                    if not operator:
                        operator = '+'
                        
                    region = pos_to_region[pos]
                    regions_operators_results.append((region, operator, result))

        return regions_operators_results
