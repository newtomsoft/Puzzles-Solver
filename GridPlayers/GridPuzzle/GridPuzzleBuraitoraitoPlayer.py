from rebrowser_playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleBuraitoraitoPlayer(PlaywrightPlayer):
    game_name = "bright-light"

    def __init__(self, browser: BrowserContext):
        super().__init__(browser)

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        
        for position, solution_value in [(position, solution_value) for position, solution_value in solution if solution_value == 1]:
            index = position.r * solution.columns_number + position.c
            await cells[index].click(click_count=2)

        await self.close()
        await self._process_video(video, rectangle, 0)
