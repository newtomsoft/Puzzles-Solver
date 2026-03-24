from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleCirclesAndSquaresPlayer(PlaywrightPlayer):
    game_name = "circles_and_squares"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        # Basic implementation to interact with the grid
        cells = await page.query_selector_all("div.g_cell")
        
        # For Circles and Squares, we need to blacken cells according to the solution
        # Assuming solution contains True for black cells, False for white cells
        for position, solution_value in [(position, solution_value) for position, solution_value in solution if solution_value is True]:
            index = position.r * solution.columns_number + position.c
            await cells[index].click()

        await self.close()
        await self._process_video(video, rectangle, 0)