from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleIslandPlayer(PlaywrightPlayer):
    """
    Player pour le puzzle Island sur gridpuzzle.com.
    Implémente les interactions pour cliquer sur les cellules selon la solution.
    """
    game_name = "island"

    async def play(self, solution: Grid):
        """
        Reçoit la grille solution et effectue les clics nécessaires sur la page web.
        """
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        # En général, gridpuzzle utilise des div avec la classe g_cell
        cells = await page.query_selector_all("div.g_cell")

        # Supposant que value == True signifie "mettre de l'eau" ou "noircir"
        for position_index in [position.r * solution.columns_number + position.c for position, value in solution if value]:
            # TODO: Confirmer la logique de clic (simple clic pour eau, double pour point, etc.)
            await cells[position_index].click()

        await self.close()
        await self._process_video(video, rectangle, 0)
