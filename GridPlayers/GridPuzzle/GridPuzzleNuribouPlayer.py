from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer

class GridPuzzleNuribouPlayer(PlaywrightPlayer):
    """
    Player pour le puzzle Nuribou sur gridpuzzle.com.
    Implémente les interactions pour cliquer sur les cellules selon la solution.
    """
    game_name = "nuribou"

    async def play(self, solution: Grid):
        """
        Reçoit la grille solution et effectue les clics nécessaires sur la page web.
        """
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        # gridpuzzle utilise des div avec la classe g_cell
        cells = await page.query_selector_all("div.g_cell")

        # Nuribou solution: BLACK (-1) ou EMPTY (0).
        # On suppose que cliquer sur la cellule la noircit.
        # Agréger les cellules noires en segments connectés puis compléter
        # chaque segment entièrement avant de passer au suivant.
        shapes = list(solution.get_all_shapes(value=-1))
        # Trier les segments par leur position minimale (haut→bas, puis gauche→droite)
        def _min_pos(s):
            return min(s, key=lambda p: (p.r, p.c))
        shapes.sort(key=lambda s: (_min_pos(s).r, _min_pos(s).c))

        for shape in shapes:
            # itérer les positions du segment en ordre ligne-major (haut→bas, gauche→droite)
            positions = sorted(list(shape), key=lambda p: (p.r, p.c))
            for position in positions:
                position_index = position.r * solution.columns_number + position.c
                await cells[position_index].click()

        await self.close()
        await self._process_video(video, rectangle, 0)
