from Domain.Board.Grid import Grid
from Domain.Puzzles.Toichika.ToichikaSolver import ToichikaSolver
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleToichikaPlayer(PlaywrightPlayer):
    game_name = "toichika"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")

        arrow_map = {
            ToichikaSolver.Up: 'arrow-up',
            ToichikaSolver.Down: 'arrow-down',
            ToichikaSolver.Right: 'arrow-right',
            ToichikaSolver.Left: 'arrow-left',
        }

        for position, solution_value in [(position, solution_value) for position, solution_value in solution if solution_value in arrow_map]:
            index = position.r * solution.columns_number + position.c
            cell = cells[index]
            cell_classes = await cell.get_attribute('class') or ''
            if 'sys_arrow' in cell_classes:
                continue
            await cell.click()
            arrow_src_part = arrow_map[solution_value]
            arrow_selector = f"img.ipt_btn[src*='{arrow_src_part}']"
            await page.wait_for_selector(arrow_selector, state="visible", timeout=2000)
            await page.click(arrow_selector)

        await self.close()
        await self._process_video(video, rectangle, 0)
