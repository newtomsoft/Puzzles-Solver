from playwright.async_api import Page
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class GridPuzzleKazokuPlayer(PlaywrightPlayer):
    game_name = "kazoku"

    async def play(self, solution: Grid) -> PlayStatus:
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)
        
        # En Kazoku, la solution est une grille d'IDs de régions.
        # On doit tracer les bordures entre les régions différentes.
        
        for r in range(solution.rows_number):
            for c in range(solution.columns_number):
                pos = Position(r, c)
                region_id = solution.value(pos)
                
                # Vérifier la bordure droite
                if c < solution.columns_number - 1:
                    right_pos = Position(r, c + 1)
                    if solution.value(right_pos) != region_id:
                        await self._draw_border(page, pos, Position(r, c + 1), "vertical", cell_width, cell_height, x0, y0)
                
                # Vérifier la bordure basse
                if r < solution.rows_number - 1:
                    down_pos = Position(r + 1, c)
                    if solution.value(down_pos) != region_id:
                        await self._draw_border(page, pos, Position(r + 1, c), "horizontal", cell_width, cell_height, x0, y0)

        await self.close()
        await self._process_video(video, rectangle)
        return PlayStatus.SUCCESS

    async def _draw_border(self, page: Page, pos1: Position, pos2: Position, orientation: str, cell_width, cell_height, x0, y0):
        # Sur gridpuzzle.com, pour Kazoku, on clique sur la ligne entre deux cellules pour ajouter/enlever une bordure.
        if orientation == "vertical":
            # Entre (r, c) et (r, c+1)
            x = x0 + (pos1.c + 1) * cell_width
            y = y0 + (pos1.r + 0.5) * cell_height
        else:
            # Entre (r, c) et (r+1, c)
            x = x0 + (pos1.c + 0.5) * cell_width
            y = y0 + (pos1.r + 1) * cell_height
            
        await page.mouse.click(x, y)
